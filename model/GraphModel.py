from flask import make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import service.MatchDataService as match_data_service
import service.SummonerDataService as summoner_data_service
import io


def build_graph_using_summoner_name(summoner_name):
    #Get all the summoner data
    summoner = summoner_data_service.get_summoner_data(summoner_name)

    #Get the solo queue match history within the summoner data
    solo_matches = match_data_service.get_solo_queue_match_list(summoner)

    #Get the latest match from the list of solo queue matches
    latest_match = solo_matches["matches"][1]

    #Get specific data about the latest match
    match_specific_data = match_data_service.get_match_specific_data(latest_match)

    #return the resulting scatter plot graph given the most recent match data
    return get_graph_model(match_specific_data)


def get_graph_model(fetched_match_data):
    x = []
    y = []
    dragons = []
    barons = []
    herald = []

    plt.xlabel = "Timestamp"
    plt.ylabel = "Number of Wards Placed"

    for match_frame_dto in fetched_match_data["frames"]:
        countWards = 0
        for match_event_dto in match_frame_dto["events"]:
            if match_event_dto["type"] == "WARD_PLACED":
                countWards += 1

            if match_event_dto["type"] == "ELITE_MONSTER_KILL" \
                    and match_event_dto["monsterType"] == "DRAGON":
                dragons.append([match_frame_dto["timestamp"] / 1000, match_event_dto["monsterSubType"]])

            if match_event_dto["type"] == "ELITE_MONSTER_KILL" \
                    and match_event_dto["monsterType"] == "BARON_NASHOR":
                barons.append(match_event_dto["timestamp"] / 1000)

            if match_event_dto["type"] == "ELITE_MONSTER_KILL" \
                    and match_event_dto["monsterType"] == "RIFTHERALD":
                herald.append(match_event_dto["timestamp"] / 1000)

        x.append(match_frame_dto["timestamp"] / 1000)
        y.append(countWards)

    return build_graph(x, y, barons, dragons, herald)


def build_graph(x,y,barons,dragons,herald):
    #These booleans are here so there are no repeated lines in the legend of the graph
    mountain = False
    cloud = False
    infernal = False
    ocean = False
    elder = False
    baron = False

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    axis.set_xlabel("Time (seconds)")
    axis.set_ylabel("Number of Wards")
    axis.set_title("Wards Placed Over Time")

    #If Rift Herald was taken in the game, mark it
    if herald is not None:
        axis.axvline(herald[0], ls='--', color='c', label="RIFT")

    #Draw the vertical lines for each dragon taken
    for line in dragons:
        if line[1] == "EARTH_DRAGON" and not mountain:
            axis.axvline(line[0], ls='--', color='g', label="MOUNTAIN")
            mountain = True
        elif line[1] == "EARTH_DRAGON" and mountain:
            axis.axvline(line[0], ls='--', color='g')

        if line[1] == "AIR_DRAGON" and not cloud:
            axis.axvline(line[0], ls='--', color='y', label="CLOUD")
            cloud = True
        elif line[1] == "AIR_DRAGON" and cloud:
            axis.axvline(line[0], ls='--', color='y')

        if line[1] == "FIRE_DRAGON" and not infernal:
            axis.axvline(line[0], ls='--', color='r', label="INFERNAL")
            infernal = True
        elif line[1] == "FIRE_DRAGON" and infernal:
            axis.axvline(line[0], ls='--', color='r')

        if line[1] == "WATER_DRAGON" and not ocean:
            axis.axvline(line[0], ls='--', color='b', label="OCEAN")
            ocean = True
        elif line[1] == "WATER_DRAGON" and ocean:
            axis.axvline(line[0], ls='--', color='b')

        if line[1] == "ELDER_DRAGON" and not elder:
            axis.axvline(line[0], ls='--', color='k', label="ELDER")
            elder = True
        elif line[1] == "ELDER_DRAGON" and elder:
            axis.axvline(line[0], ls='--', color='k')

    #Draw the vertical lines for each Baron that was taken
    for line in barons:
        if baron:
            axis.axvline(line, ls='--', color='m', label="BARON")
            baron = True
        else:
            axis.axvline(line, ls='--', color='m')

    axis.scatter(x, y)
    axis.legend(loc='best')

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'

    return response
