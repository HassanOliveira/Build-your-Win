import requests

class RiotAPI:
    def __init__(self, api_key, region):
        self.api_key = api_key
        self.region = region

    def _request(self, endpoint, params=None):
        url = f"https://{self.region}.api.riotgames.com{endpoint}"
        headers = {"X-Riot-Token": self.api_key}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_summoner_id(self, summoner_name):
        endpoint = f"/lol/summoner/v4/summoners/by-name/{summoner_name}"
        return self._request(endpoint)['id']

    def get_live_game_data(self, summoner_id):
        endpoint = f"/lol/spectator/v4/active-games/by-summoner/{summoner_id}"
        return self._request(endpoint)

    def get_all_items(self):
        url = f"http://ddragon.leagueoflegends.com/cdn/14.12.1/data/en_US/item.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
