class ItemRecommender:
    def __init__(self, game_data):
        self.game_data = game_data

    def recommend_item(self):
        # Implementar lógica avançada de recomendação de itens aqui
        # Exemplo simples:
        participants = self.game_data['participants']
        for participant in participants:
            print(f"Player: {participant['summonerName']}, Suggested Item: Example Item")
        # Devolva as sugestões de itens conforme a lógica implementada
