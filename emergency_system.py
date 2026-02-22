
class EmergencySystem():

    def emergency_system(self, func:typing.Callable, *args, **kwargs):
        
        emergency_moves = ["left", "right", "up", "down"]

        try: 
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            EmergencyLogger.loger_queue.put((func.__name__, e, self.turn_counter))
            if func.__name__ == "reset_is_move_safe":
                self.is_move_safe = {"left": {"is_safe": True, "priority": 0}, 
                                 "right": {"is_safe": True, "priority": 0},
                                 "up": {"is_safe": True, "priority": 0},
                                 "down": {"is_safe": True, "priority": 0}}
                return None
            else:
                try:
                    next_move = random.choice(emergency_moves)
                    return {"move": next_move, "id": "Emergency!"}
                except Exception as e:
                    EmergencyLogger.loger_queue.put((func.__name__, f"{e}", self.turn_counter))
                    return {"move": "down", "id": "Emergency!"}
                
    def is_emergency(self, result):

        if isinstance(result, dict):
            if "id" in result:
                if result["id"] == "Emergency!":
                    return True
                
        return False