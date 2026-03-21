import logging
import os
import typing

from flask import Flask
from flask import request , jsonify , abort

from functools import wraps

from validate_game_state import validate_game_state

import os

# Sets up and runs the Flask server on a fixed port.
class Server():

    def __init__(self, handlers: typing.Dict, port, logger_name, logger_file, debug):

        self.app = Flask("Battlesnake")
        
        self.handlers = handlers
        self.port = port
        self.logger_name = logger_name
        self.logger_file = logger_file
        self.debug = debug

        self.setup_routes()



    # Registers all API routes and their handlers.
    def setup_routes(self):

        @self.app.get("/")
        def on_info():
            # returns snake appearance and metadata
            try:
                return self.handlers["info"]()
            except Exception as e:
                return jsonify({"error": f"Info not available: {e}"})

        @self.app.post("/start")
        def on_start():
            # initializes logger and resets state for a new game
            game_state = request.get_json()
            if not validate_game_state(game_state):
                print("Game state validation failed")
                return jsonify({"error": "Game state validation failed"}), 400
            try:
                self.handlers["start"](game_state, self.logger_name, self.logger_file, self.debug)
                return jsonify({"status": "ok"})
            except Exception as e:
                print(f"Error: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.post("/move")
        def on_move():
            # returns the next move for the current turn
            game_state = request.get_json()
            if not validate_game_state(game_state):
                print("Game state validation failed")
                return jsonify({"error": "Game state validation failed"}), 400
            try:
                return self.handlers["move"](game_state)
            except Exception as e:
                print(f"Error: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.post("/end")
        def on_end():
            # stops the logging worker and clears the logger
            game_state = request.get_json()
            if not validate_game_state(game_state):
                print("Game state validation failed")
                return jsonify({"error": "Game state validation failed"}), 400
            try:
                self.handlers["end"](game_state)
                return jsonify({"status": "ok"})
            except Exception as e:
                print(f"Error: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.get("/admin/push")
        @self.admin_required
        def on_push():
            # pushes logs to remote git repository
            try:
                return self.handlers["push"]()
            except Exception as e:
                print(f"Error: {e}")
                return jsonify({"error": f"Failed to push to git: {e}"}), 500

        @self.app.after_request
        def identify_server(response):
            # adds server identification header to every response
            response.headers.set("server", "battlesnake/github/starter-snake-python")
            return response
        
    # Decorator that protects admin routes by validating the admin token.
    # Expects the token in the X-Admin-Token request header.
    def admin_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = os.environ.get("ADMIN_TOKEN")
            if token != request.headers.get("X-Admin-Token"):
                abort(403)
            return f(*args, **kwargs)
        return decorated
        
    # Starts the Flask server on all network interfaces.
    def run_server(self):
        self.app.run(host="0.0.0.0", port=self.port)
