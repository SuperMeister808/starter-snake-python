
import typing

import random

from logger.emergency_logger import EmergencyLogger

# Wraps callable functions in a fallback system — guarantees a move
# is always returned even if a calculation raises an exception.
class EmergencySystem():
    
    def __init__(self, move):

        self.move = move
    
    # Wraps a function call in a fallback system.
    # Returns an emergency move if the function raises an exception.
    # Falls back to "down" if even the emergency move selection fails.
    def emergency_system(self, func: typing.Callable, *args, **kwargs):

        EMERGENCY_MOVES = ["left", "right", "up", "down"]
        EMERGENCY_ID = "Emergency!"

        try:
            return func(*args, **kwargs)
        except Exception as e:
            EmergencyLogger.loger_queue.put((func.__name__, e, self.move.turn_counter, 40))

            # fallback — return a random emergency move
            try:
                return {"move": random.choice(EMERGENCY_MOVES), "id": EMERGENCY_ID}
            except Exception as e:
                EmergencyLogger.loger_queue.put((func.__name__, e, self.move.turn_counter, 40))

                # last resort fallback — hardcoded move if random.choice fails
                return {"move": "down", "id": EMERGENCY_ID}
                
    # Returns True if the result is an emergency fallback move.
    def is_emergency(self, result):
        return isinstance(result, dict) and result.get("id") == "Emergency!"