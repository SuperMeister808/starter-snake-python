import logging
import os
import typing

from flask import Flask
from flask import request

from validate_game_state import validate_game_state


def run_server(handlers: typing.Dict, port):
    app = Flask("Battlesnake")
    
    @app.get("/")
    def on_info():
        return handlers["info"]()

    @app.post("/start")
    def on_start():
        game_state = request.get_json()
        if validate_game_state(game_state):
            handlers["start"](game_state)
            return "ok"
        else:
            return "Game State Validation Failed!" , 400

    @app.post("/move")
    def on_move():
        game_state = request.get_json()
        if validate_game_state(game_state):
            return handlers["move"](game_state)
        else:
            return "Game State Validation Failed!" , 400

    @app.post("/end")
    def on_end():
        game_state = request.get_json()
        if validate_game_state(game_state):
            handlers["end"](game_state)
            return "ok"
        else:
            return "Game State Validation Failed!" , 400

    @app.after_request
    def identify_server(response):
        response.headers.set(
            "server", "battlesnake/github/starter-snake-python"
        )
        return response

    host = "0.0.0.0"

    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print(f"\nRunning Battlesnake at http://{host}:{port}")
    app.run(host=host, port=port)
