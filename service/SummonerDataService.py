import json
import requests
import utilities.PropertyDefinitions as properties

api_key = properties.api_key


def get_summoner_data(summoner_name):
    api_summoner = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name

    headers = {
        'Content-Type': 'application/json',
        'X-Riot-Token': api_key}

    response = requests.get(api_summoner, headers=headers)

    return json.loads(response.text)
