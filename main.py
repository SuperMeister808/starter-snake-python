# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import threading

from move import Move
from emergency_logger import EmergencyLogger

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
class ServerHandler():

    def info(self) -> typing.Dict:
        print("INFO")

        return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#FF0000",  
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
        }

    def print_game_state(self, game_state: typing.Dict):
        print(game_state)

    # start is called when your Battlesnake begins a game
    def start(self, game_state: typing.Dict):
    
        EmergencyLogger.is_running = True
        thread = threading.Thread(target=EmergencyLogger.log_worker)
        thread.start()
        EmergencyLogger.worker_thread = thread
        return "GAME START"


    # end is called when your Battlesnake finishes a game
    def end(self, game_state: typing.Dict):
        EmergencyLogger.is_running = False
        EmergencyLogger.worker_thread.join()
        try:
            EmergencyLogger.upload_to_git()
        except Exception as e:
            return f"Git Upload failed: {e}"
        return "GAME OVER\n"

    # move is called on every turn and returns your next move
    # Valid moves are "up", "down", "left", or "right"
    # See https://docs.battlesnake.com/api/example-move for available data
    def move(self, game_state: typing.Dict) -> typing.Dict:

        next_move = Move()
        game_move = next_move.choose_move(game_state)

        return game_move

    

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import Server

    server_handler = ServerHandler()
    app = Server({"info": server_handler.info, "start": server_handler.start, "move": server_handler.move, "end": server_handler.end}, 8000)

    app.run_server()
