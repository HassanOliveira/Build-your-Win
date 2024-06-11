from riot_api import RiotAPI
from item_recommender import ItemRecommender
from database import Database
import config
import requests

def main():
    api = RiotAPI(config.API_KEY, config.REGION)
    db = Database(config.DATABASE)
    
    try:
        # Obter todos os itens e armazenar no banco de dados
        items_data = api.get_all_items()
        for item_id, item in items_data['data'].items():
            db.insert_item(item_id, item['name'], item['description'], item['gold']['total'])
        
        print("Items stored in database successfully.")
        
        # Processar dados do jogo em tempo real
        summoner_id = api.get_summoner_id(config.SUMMONER_NAME)
        game_data = api.get_live_game_data(summoner_id)
        
        recommender = ItemRecommender(game_data)
        recommender.recommend_item()
        
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
