
import typing

import random

from emergency_logger import EmergencyLogger
from move import Move

class EmergencySystem():
    
    def __init__(self):

        self.move = Move()
    
    def emergency_system(self, func:typing.Callable, *args, **kwargs):
        
        emergency_moves = ["left", "right", "up", "down"]

        try: 
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            EmergencyLogger.loger_queue.put((func.__name__, e, self.move.turn_counter))
            try:
                next_move = random.choice(emergency_moves)
                return {"move": next_move, "id": "Emergency!"}
            except Exception as e:
                EmergencyLogger.loger_queue.put((func.__name__, f"{e}", self.move.turn_counter))
                return {"move": "down", "id": "Emergency!"}
                
    def is_emergency(self, result):

        if isinstance(result, dict):
            if "id" in result:
                if result["id"] == "Emergency!":
                    return True
                
        return False