import requests
import threading
import berserk
import time
from lichess_client import APIClient
from dotenv import load_dotenv
import os

load_dotenv()


class Fetch:
    def __init__(self):
        # self.api_token = os.getenv("api_token")
        self.game_id = "game_id"
        # self.headers = {"Authorization":f'Bearer {self.api_token}' ,'Accept':"application/x-ndjson"}
        self.url = f"https://api.chess.com/pub/game/{self.game_id}/stream"
        self.token = os.getenv("lichess_token") 

        self.session = berserk.TokenSession(self.token)
        self.client = berserk.Client(session=self.session)





    def stream_lichess_game_by_id(self,lichess_game_string_id):

        while True:
            # Fetch the current state of the game
            game_state = self.client.games.export(lichess_game_string_id)
            # print(game_state)

            # Get the PGN position from the game state
            pgn_position = game_state['moves']

            # print(f"FEN Position: {pgn_position}")
            time.sleep(5)

            yield pgn_position

        


