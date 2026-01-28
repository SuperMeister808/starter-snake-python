import logging
import os
import typing

from flask import Flask
from flask import request , jsonify , abort

from functools import wraps

from validate_game_state import validate_game_state

import os


class Server():

    def __init__(self, handlers: typing.Dict, port):

        self.app = Flask("Battlesnake")
        
        self.handlers = handlers

        self.port = port

        self.setup_routes()



    def setup_routes(self):

        @self.app.get("/")
        def on_info(): 
            try:
                return self.handlers["info"]()
            except Exception as e:
                return jsonify({"Error": f"Infos not available: {e}"})

        @self.app.post("/start")
        def on_start():
            game_state = request.get_json()
            if validate_game_state(game_state):
                try:
                    self.handlers["start"](game_state)
                    return jsonify({"status": "ok"})
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
                    return jsonify({"status": "ok"})
                except Exception as e:
                    print(f"Error: {e}")
                    return jsonify({"Error": f"Error: {e}"}) , 500
            else:
                print("Game State Validation Failed!")
                return jsonify({"Error": "Game State Validation Failed!"}) , 400
            
        @self.app.get("/admin/push")
        @self.admin_required
        def on_push():
            
            try:
                self.handlers["push"]()
                return jsonify({"status": "ok"})
            except Exception as e:
                return jsonify({"Error": f"Failed to push on git:{e}"}) , 500
            
        @self.app.after_request
        def identify_server(response):
            response.headers.set(
                "server", "battlesnake/github/starter-snake-python"
            )
            return response
        
    def admin_required(self, f):

        @wraps(f)
        def decorated(*args, **kwargs):
            token = os.environ.get("ADMIN_TOKEN")

            if token != request.headers.get("X-Admin-Token"):
                abort(403)
            return f(*args, **kwargs)
        
        return decorated
        
    def run_server(self):

        host = "0.0.0.0"

        self.app.run(host=host, port=self.port)
