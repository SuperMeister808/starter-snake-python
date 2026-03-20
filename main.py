# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#

import random
import typing
import threading

import time

from move import Move
from logger.emergency_logger import EmergencyLogger

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
class ServerHandler():

    # Returns the snake's appearance and author metadata.
    # Customize color, head and tail on the Battlesnake website.
    def info(self) -> typing.Dict:
        return {
            "apiversion": "1",
            "author": "",
            "color": "#FF0000",
            "head": "default",
            "tail": "default",
        }

    # Prints the full game state for debugging purposes.
    def print_game_state(self, game_state: typing.Dict):
        print(game_state)

    # Called when a new game starts.
    # Resets state, sets up the logger and starts the async logging worker thread.
    def start(self, game_state: typing.Dict, logger_name, logger_file, debug):

        try:
            Move.reset_turn_counter()
            EmergencyLogger.setup_runtime_logger(logger_name, logger_file, debug)
            EmergencyLogger.flags["is_running"] = True
            thread = threading.Thread(target=EmergencyLogger.log_worker)
            thread.start()
            EmergencyLogger.flags["worker_thread"] = thread
        except Exception as e:
            print(f"Threading failed: {e}")

    # Called when a game ends.
    # Signals the logging worker to stop, waits for it to finish, then clears the logger.
    def end(self, game_state: typing.Dict):

        try:
            EmergencyLogger.flags["is_running"] = False
            worker_thread = EmergencyLogger.flags["worker_thread"]
            worker_thread.join()
            EmergencyLogger.clear_emergency_logger()
        except Exception as e:
            print(f"Thread could not join: {e}")
            EmergencyLogger.clear_emergency_logger()

    # Pushes logs to the remote git repository after the game ends.
    def push(self):
        return EmergencyLogger.push_to_git()

    # Called on every turn — creates a Move instance and returns the selected move.
    def move(self, game_state: typing.Dict) -> typing.Dict:
        next_move = Move()
        return next_move.choose_move(game_state)

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import Server

    server_handler = ServerHandler()

    handlers = {
        "info":  server_handler.info,
        "start": server_handler.start,
        "move":  server_handler.move,
        "end":   server_handler.end,
        "push":  server_handler.push,
    }

    app = Server(handlers, 8000, "RuntimeLogger", "runtime.log", False)
    app.run_server()
