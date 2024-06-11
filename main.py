from riot_api import RiotAPI
from item_recommender import ItemRecommender
import config, requests

def main():
    api = RiotAPI(config.API_KEY, config.REGION)
    
    try:
        summoner_id = api.get_summoner_id(config.SUMMONER_NAME)
        game_data = api.get_live_game_data(summoner_id)
        
        recommender = ItemRecommender(game_data)
        recommender.recommend_item()
        
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()
