
import typing

import random

from logger.emergency_logger import EmergencyLogger

class EmergencySystem():
    
    def __init__(self, move):

        self.move = move
    
    def emergency_system(self, func:typing.Callable, *args, **kwargs):
        
        emergency_moves = ["left", "right", "up", "down"]

        try: 
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            EmergencyLogger.loger_queue.put((func.__name__, e, self.move.turn_counter, 40))
            try:
                next_move = random.choice(emergency_moves)
                return {"move": next_move, "id": "Emergency!"}
            except Exception as e:
                EmergencyLogger.loger_queue.put((func.__name__, e, self.move.turn_counter, 40))
                return {"move": "down", "id": "Emergency!"}
                
    def is_emergency(self, result):

        if isinstance(result, dict):
            if "id" in result:
                if result["id"] == "Emergency!":
                    return True
                
        return False