import logging
import os
import typing

from flask import Flask
from flask import request , jsonify

from validate_game_state import validate_game_state


class Server():

    def __init__(self, handlers: typing.Dict, port):

        self.app = Flask("Battlesnake")
        
        self.handlers = handlers

        self.port = port

        self.setup_routes()



    def setup_routes(self):

        @self.app.get("/")
        def on_info():
            return self.handlers["info"]()

        @self.app.post("/start")
        def on_start():
            game_state = request.get_json()
            if validate_game_state(game_state):
                try:
                    self.handlers["start"](game_state)
                    return "ok"
                except Exception as e:
                    print(f"Error: {e}")
                    return jsonify({"Error": f"{e}"})
            else:
                print("Game State Validation Failed!")
                return jsonify({"Error": "Game State Validation Failed!"}) , 400

        @self.app.post("/move")
        def on_move():
            game_state = request.get_json()
            if validate_game_state(game_state):
                try:
                    return self.handlers["move"](game_state)
                except Exception as e:
                    print(f"Error: {e}")
                    return jsonify({"Error": f"{e}"}) , 500
            else:
                print("Game State Validation Failed!")
                return jsonify({"Error": "Game State Validation Failed"}) , 400


        @self.app.post("/end")
        def on_end():
            game_state = request.get_json()
            if validate_game_state(game_state):
                try:
                    self.handlers["end"](game_state)
                except Exception as e:
                    print(f"Error: {e}")
                    return jsonify({"Error": f"Error: {e}"}) , 500
            else:
                print("Game State Validation Failed!")
                return jsonify({"Error": "Game State Validation Failed!"}) , 400
            
        @self.app.after_request
        def identify_server(response):
            response.headers.set(
                "server", "battlesnake/github/starter-snake-python"
            )
            return response
        
    def run_server(self):

        host = "0.0.0.0"

        logging.getLogger("werkzeug").setLevel(logging.ERROR)

        print(f"\nRunning Battlesnake at http://{host}:{self.port}")
        self.app.run(host=host, port=self.port)
