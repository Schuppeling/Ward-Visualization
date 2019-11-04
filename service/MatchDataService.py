import json
import requests
import utilities.PropertyDefinitions as properties

api_key = properties.api_key
solo_queue_id = properties.solo_queue_id


def get_match_specific_data(match):
    match_id = match["gameId"]
    apiMatch = "https://na1.api.riotgames.com/lol/match/v4/timelines/by-match/" + str(match_id)

    headers = {
        'Content-Type': 'application/json',
        'X-Riot-Token': api_key}

    response = requests.get(apiMatch, headers=headers)

    return response.json()


def get_solo_queue_match_list(summonerData):
    account_id = summonerData['accountId']
    url = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + account_id + "?queue=" + solo_queue_id

    headers = {
        'Content-Type': 'application/json',
        'X-Riot-Token': api_key}

    response = requests.get(url, headers=headers)

    return json.loads(response.text)
