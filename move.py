
import random

from git import Repo

import threading

import typing

import copy

from emergency_logger import EmergencyLogger

class Move():

    def __init__(self):

        self.is_move_safe = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}
        
        self.is_move_safe_memory = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}
        
        self.opponents_positions = {}
        
        self.turn_counter = 0


    def not_backward(self, **kwargs):

        NEEDED_KEYWORDS = ["head", "neck"]

        head , neck = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)

            
        if neck["x"] < head["x"]:  
            self.is_move_safe["left"]["is_safe"] = False

        elif neck["x"] > head["x"]:  
            self.is_move_safe["right"]["is_safe"] = False

        elif neck["y"] < head["y"]:  
            self.is_move_safe["down"]["is_safe"] = False

        elif neck["y"] > head["y"]: 
            self.is_move_safe["up"]["is_safe"] = False         



       
    def not_wall_collision(self, **kwargs):

        NEEDED_KEYWORDS = ["head", "game_state"]

        head, game_state = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)


        board_width = game_state["board"]["width"]
        board_height = game_state["board"]["height"]
    
        if head["x"] == board_width -1:

            self.is_move_safe["right"]["is_safe"] = False

        if head["x"] == 0:

            self.is_move_safe["left"]["is_safe"] = False

        if head["y"] == board_height -1:

            self.is_move_safe["up"]["is_safe"] = False

        if head["y"] == 0:

            self.is_move_safe["down"]["is_safe"] = False

    def not_itself_collision(self, **kwargs):

        NEEDED_KEYWORDS = ["head", "body"]
        

        head, body = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)


        position_x = head["x"]

        position_y = head["y"]
        
        for e in body[1:]:

            x = e["x"]
            y = e["y"]

            if (position_x) + 1 == x and position_y == y:

                self.is_move_safe["right"]["is_safe"] = False

            if (position_x) - 1 == x and position_y == y:

                self.is_move_safe["left"]["is_safe"] = False

            if (position_y) + 1 == y and position_x == x:

                self.is_move_safe["up"]["is_safe"] = False

            if (position_y) - 1 == y and position_x == x:

                self.is_move_safe["down"]["is_safe"] = False

    def not_enemy_collision(self, **kwargs):
        
        NEEDED_KEYWORDS = ["head", "game_state"]

        head, game_state = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)


        first_move = {"x": head["x"] + 1, "y": head["y"]}

        second_move = {"x": head["x"] - 1, "y": head["y"]}

        third_move = {"x": head["x"], "y": head["y"] + 1}

        fourth_move = {"x": head["x"], "y": head["y"] - 1}

        for snake , position in self.opponents_positions.items():
                
            if snake != game_state["you"]["id"]:
            
                for entry in position["unsafe"]:
            
                    if entry == first_move:

                        self.is_move_safe["right"]["is_safe"] = False

                    if entry == second_move:

                        self.is_move_safe["left"]["is_safe"] = False

                    if entry == third_move:

                        self.is_move_safe["up"]["is_safe"] = False

                    if entry == fourth_move:

                        self.is_move_safe["down"]["is_safe"] = False

                for entry in position["priority"]:

                    if entry == first_move:

                        self.is_move_safe["right"]["priority"] += 1

                    if entry == second_move:

                        self.is_move_safe["left"]["priority"] += 1

                    if entry == third_move:

                        self.is_move_safe["up"]["priority"] += 1

                    if entry == fourth_move:

                        self.is_move_safe["down"]["priority"] += 1

    def is_growing(self, **kwargs):

        NEEDED_KEYWORDS = ["snake", "game_state"]

        snake , game_state = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)


        head = snake["head"]

        food = game_state["board"]["food"]

        for entry in food:

            if entry == {"x": head["x"] + 1,"y": head["y"]}:

                return True
            
            if entry == {"x": head["x"] - 1, "y": head["y"]}:

                return True
            
            if entry == {"x": head["x"], "y": head["y"] + 1}:

                return True
            
            if entry == {"x": head["x"], "y": head["y"] - 1}:

                return True
            
        return False

    def calculate_opponents_positions(self, **kwargs):

        NEEDED_KEYWORDS = ["game_state"]

        game_state, = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        
        positions = {}
        
        snakes = game_state["board"]["snakes"]
        
        for snake in snakes:

            if not isinstance(snake, dict):
                continue

            required_snake_keys = ["id", "head", "length", "body"]
            if any(key not in snake for key in required_snake_keys):
                continue

            positions [snake["id"]] = {"unsafe": [],"priority": []}
            positions [snake["id"]]["unsafe"].append(snake["head"])
                
            my_length = game_state["you"]["length"]
            opponent_length = snake["length"]
                          
            first_move = {"x": snake["head"]["x"] + 1, "y": snake["head"]["y"]}
            second_move = {"x": snake["head"]["x"] - 1, "y": snake["head"]["y"]}
            third_move = {"x": snake["head"]["x"], "y": snake["head"]["y"] + 1}
            fourth_move = {"x": snake["head"]["x"], "y": snake["head"]["y"] - 1}      
                
            moves = [first_move, second_move, third_move, fourth_move]      

            positions[snake["id"]]["priority"].extend(moves)
            if opponent_length >= my_length:
                positions[snake["id"]]["unsafe"].extend(moves)

            for i , body_part in enumerate(snake["body"]):

                if i != len(snake["body"]) - 1:
                    
                    positions[snake["id"]]["unsafe"].append(body_part)
                else:
                    try:
                        if self.is_growing(snake=snake, game_state=game_state):

                            positions[snake["id"]]["unsafe"].append(snake["body"][-1])
                    except Exception:
                        raise

        return positions
    
    def reset_is_move_safe(self, **kwargs):
        
        self.is_move_safe = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}

    def reset_is_move_safe_memory(self, **kwargs):
        
        self.is_move_safe_memory = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}

    
    def calculate_food(self, **kwargs):
        
        NEEDED_KEYWORDS = ["head", "game_state"]

        head, game_state = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        
        food_list = game_state["board"]["food"]

        left_move = {"x": head["x"] -1, "y": head["y"]}
        right_move = {"x": head["x"] + 1, "y": head["y"]}
        up_move = {"x": head["x"], "y": head["y"] + 1}
        down_move = {"x": head["x"], "y": head["y"] - 1}

        for item in food_list:

            if left_move["x"] == item["x"] and left_move["y"] == item["y"]:

                self.is_move_safe["left"]["priority"] += 1

            if right_move["x"] == item["x"] and right_move["y"] == item["y"]:

                self.is_move_safe["right"]["priority"] += 1

            if up_move["x"] == item["x"] and up_move["y"] == item["y"]:

                self.is_move_safe["up"]["priority"] += 1

            if down_move["x"] == item["x"] and down_move["y"] == item["y"]:

                self.is_move_safe["down"]["priority"] += 1

    def future_safety(self, relevant_position:typing.List[dict]=None, **kwargs):
            
            NEEDED_KEYWORDS = ["head", "game_state", "body", "neck"]

            head, game_state, body, neck = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)

            
            if relevant_position is None:
                
                relevant_position = []

                
                move_left = {"x": head["x"] - 1, "y": head["y"]}
                move_right = {"x": head["x"] + 1, "y": head["y"]}
                move_up = {"x": head["x"], "y": head["y"] + 1}
                move_down = {"x": head["x"], "y": head["y"] - 1}
                possible_moves = [move_left, move_right, move_up, move_down]
            
                relevant_position.extend(possible_moves)

            safe_move_left = False
            new_relevant_positions = []
            
            for e in relevant_position:
                
                self.reset_is_move_safe(**kwargs)

                result = self.check_moves(head=e, game_state=game_state, body=body, neck=neck)

                for move , data in self.is_move_safe.items():
                    if data["is_safe"] == True:
                        safe_move_left = True
                
                        
                        move_left = {"x": e["x"] - 1, "y": e["y"]}
                        move_right = {"x": e["x"] + 1, "y": e["y"]}
                        move_up = {"x": e["x"], "y": e["y"] + 1}
                        move_down = {"x": e["x"], "y": e["y"] - 1}
                        possible_moves = [move_left, move_right, move_up, move_down]
                        

                        new_relevant_positions.extend(possible_moves)
   
            return safe_move_left , new_relevant_positions
    
    def call_future_safety(self, **kwargs):

            NEEDED_KEYWORDS = ["game_state", "body", "move", "calls", "head"]

            game_state , body , move , calls , head = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)


            if move == "left":
                neck = head
                head = {"x": head["x"] -1, "y": head["y"]}
            if move == "right":
                neck = head
                head = {"x": head["x"] + 1, "y": head["y"]}
            if move == "up":
                neck = head
                head = {"x": head["x"], "y": head["y"] + 1}
            if move == "down":
                neck = head
                head = {"x": head["x"], "y": head["y"] - 1}

            body = self.call_get_body(body=body, head=head)

            for i in range(calls):
            
                self.reset_is_move_safe(**kwargs)

                safe_move_left , relevant_position = self.future_safety(head=head, game_state=game_state, body=body, neck=neck)

                if safe_move_left == False:
                    return False
                
            return True

    def check_moves(self, **kwargs):
        
        NEEDED_KEYWORDS = ["head", "game_state", "body", "neck"]

        head, game_state, body, neck = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)


        checks = [self.reset_is_move_safe,
                  self.not_backward, 
                  self.not_wall_collision, 
                  self.not_itself_collision, 
                  self.not_enemy_collision, 
                  self.calculate_food]

        for check in checks:

            result = check(head=head, game_state=game_state, body=body, neck=neck)
            if self.is_emergency(result):
                return result

        
    def safe_is_move_safe(self, **kwargs):

        #copy, da dicts mutable sind
        self.is_move_safe_memory = copy.deepcopy(self.is_move_safe)


        self.reset_is_move_safe(**kwargs)


    def load_is_move_safe(self, **kwargs):

        #copy, da dicts mutable sind
        self.is_move_safe = copy.deepcopy(self.is_move_safe_memory)
        

        self.reset_is_move_safe_memory(**kwargs)


    def get_allowed_keywords(self, **kwargs):

        ALLOWED_KEYWORDS = ["head", "game_state", "body", "neck", "snake", "calls", "move", "new_head", "safe_moves", "memory_moves"]
        keywords = {}

        for allowed_keyword in ALLOWED_KEYWORDS:
            try:
                keyword = kwargs[allowed_keyword]
                keywords[allowed_keyword] = keyword
            except KeyError as e:
                continue
        
        return keywords
    
    def check_datatype(self, keywords: typing.Dict):

        DICTIONARY_KEYS = ["head", "game_state", "neck", "new_head", "safe_moves", "snake"]
        LIST_KEYS = ["body", "memory_moves"]
        STRING_KEYS = ["move"]
        INTEGER_KEYS = ["calls"]
        FLOAT_KEYS = []

        for key , keyword in keywords.items():
            
            listed = False
            
            if key in DICTIONARY_KEYS:
                listed = True
                if not isinstance(keyword, dict):
                    raise TypeError(f"{key} als Dictionary erforderlich!")
                
            if key in LIST_KEYS:
                listed = True
                if not isinstance(keyword, list):
                    raise TypeError(f"{key} als Liste erforderlich!")
                
            if key in STRING_KEYS:
                listed = True
                if not isinstance(keyword, str):
                    raise TypeError(f"{key} als String erforderlich!")
                
            if key in INTEGER_KEYS:
                listed = True
                if not isinstance(keyword, int):
                    raise TypeError(f"{key} als Integer erforderlich!")
                
            if key in FLOAT_KEYS:
                listed = True
                if not isinstance(keyword, float):
                    raise TypeError(f"{key} als Float erforderlich!")
                
            if listed == False:
                raise RuntimeError(f"{key} nicht gelisted")
    
    def extract_keywords(self, needed_keywords: typing.List[str], **kwargs):


        keywords = self.get_allowed_keywords(**kwargs)

        self.check_datatype(keywords)

        found_keywords = []
        for keyword in needed_keywords:
            if keyword not in keywords:
                raise KeyError(f"{keyword} erforderlich!")
            found_keywords.append(keywords[keyword])

        return found_keywords
    
    def get_body(self, new_body:typing.List[dict]=None, **kwargs):
        
        NEEDED_KEYWORDS = ["head"]

        head, = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        if new_body is None:
            new_body = []

        new_body.append(head)

        return new_body
        
    def call_get_body(self, **kwargs):
        
        NEEDED_KEYWORDS = ["head", "body"]
        
        head, body = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        new_body = []
        
        calls = 0

        required_calls = len(body)
        
        for body_part in body:
            
            if calls == required_calls:

                return new_body
            
            if "id" in body_part:
                required_calls = required_calls - 1
                continue

            new_body = self.get_body(new_body, head=head)

            head = body_part

            calls += 1

        return new_body

    def get_neck(self, **kwargs):

        NEEDED_KEYWORDS = ["body"]

        body, = self.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        try:
            neck = body[1]
        except IndexError:
            try:
                neck = body[0]
            except IndexError:
                raise IndexError("Body ist leer")
        
        return neck
    
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

    def get_safe_moves(self, **kwargs):

        NEEDED_KEYWORDS = ["game_state"]
    
        result = self.emergency_system(self.extract_keywords, NEEDED_KEYWORDS, **kwargs)
        if self.is_emergency(result):
            return result
        game_state = result
        
        # Are there any safe moves left?
        safe_moves = {}
        try:
            for move , data in self.is_move_safe.items():
                if data["is_safe"] == True:
                    safe_moves[move] = data["priority"]
            return safe_moves
        except Exception as e:
            EmergencyLogger.loger_queue.put(("safe_moves", f"{e}", self.turn_counter)) 
            safe_moves = {"left": 0, "right": 0, "up": 0, "down": 0} 
            return safe_moves
        
    def get_priority_moves(self, **kwargs):
        
        NEEDED_KEYWORDS = ["safe_moves", "game_state"]
        result = self.emergency_system(self.extract_keywords, NEEDED_KEYWORDS, **kwargs)
        if self.is_emergency(result):
            return result
        safe_moves , game_state = result
        
        memory_moves = []
        memory_priority = 0
        try:
            for move , priority in safe_moves.items():

                if memory_moves == [] and memory_priority == 0:

                    if priority != 0:
                
                        memory_moves.append(move)
                        memory_priority = priority
                        continue

                if memory_priority != 0:
            
                    if priority > memory_priority:

                        memory_moves.clear()
                        memory_moves.append(move)
                        memory_priority = priority
                        continue

                    if priority == memory_priority:

                        memory_moves.append(move)
                        continue
            return memory_moves
        except Exception as e:
            EmergencyLogger.loger_queue.put(("priority", f"{e}", self.turn_counter))
            memory_moves = []
            return memory_moves
        
    def random_choice(self, **kwargs):

        NEEDED_KEYWORDS = ["game_state", "safe_moves", "memory_moves"]
        result = self.emergency_system(self.extract_keywords, NEEDED_KEYWORDS, **kwargs)
        if self.is_emergency(result):
            return result
        game_state , safe_moves , memory_moves = result
        
        emergency_moves = ["left", "right", "up", "down"]
        
        try:
            next_move = random.choice(memory_moves)
            EmergencyLogger.loger_queue.put(("random_choice", "Success: Priority Move choosed", self.turn_counter))
            return {"move": next_move}
        except Exception as e:
            EmergencyLogger.loger_queue.put(("random_choice", f"No priorities set: {e}", self.turn_counter))
            try:
                keys = []
                for key , value in safe_moves.items():
                    keys.append(key)
                next_move = random.choice(keys)
                return {"move": next_move}
            except Exception as e:
                EmergencyLogger.loger_queue.put(("random_choice", f"No safe moves left: {e}", self.turn_counter))
                try:
                    next_move = random.choice(emergency_moves)
                    return {"move": next_move}
                except Exception as e:
                    EmergencyLogger.loger_queue.put(("random_choice", f"{e}", self.turn_counter))
                    return {"move": "down"}

    
    
    def choose_move(self, game_state:typing.Dict):
        
        
        try:
            head = game_state["you"]["head"]
            body = game_state["you"]["body"]
        except Exception:
            raise RuntimeError("Variabele game_state nicht vorhanden!")
        
        result = self.emergency_system(self.get_neck, body=body, game_state=game_state)
        if self.is_emergency(result):
            self.turn_counter += 1
            return {"move": result["move"]}
        neck = result

        result = self.emergency_system(self.calculate_opponents_positions, game_state=game_state)
        if self.is_emergency(result):
            self.turn_counter += 1
            return {"move": result["move"]}
        self.opponents_positions = result

        result = self.emergency_system(self.reset_is_move_safe, head=head, game_state=game_state, body=body, neck=neck)
        if self.is_emergency(result):
            self.turn_counter += 1
            return {"move": result["move"]}
        
        result = self.emergency_system(self.check_moves, head=head, game_state=game_state, body=body, neck=neck)
        if self.is_emergency(result):
            self.turn_counter += 1
            return {"move": result["move"]}
        
        result = self.emergency_system(self.get_safe_moves, game_state=game_state)
        if self.is_emergency(result):
            self.turn_counter += 1
            return {"move": result["move"]}
        
        safe_moves = result
        
        result = self.emergency_system(self.safe_is_move_safe, head=head, game_state=game_state, body=body, neck=neck)
        if self.is_emergency(result):
            self.turn_counter += 1
            return {"move": result["move"]}
        
        to_delete = []
        for move , data in safe_moves.items():
            result = self.emergency_system(self.call_future_safety, calls=2, move=move, head=head, game_state=game_state, body=body, neck=neck)
            if self.is_emergency(result):
                self.turn_counter += 1
                return {"move": result["move"]}
            if result == False:
                to_delete.append(move) 
        for key in to_delete:
            print("Delete safe_move")
            del safe_moves[key]

        result = self.emergency_system(self.load_is_move_safe, head=head, game_state=game_state, body=body, neck=neck) 
        if self.is_emergency(result):
            self.turn_counter += 1
            return {"move": result["move"]}
        
        result = self.emergency_system(self.get_priority_moves, safe_moves=safe_moves, game_state=game_state) 
        if self.is_emergency(result):
            self.turn_counter += 1
            return {"move": result["move"]}
        memory_moves = result
        
        
        result = self.random_choice(game_state=game_state, safe_moves=safe_moves, memory_moves=memory_moves)
        if self.is_emergency(result):
            self.turn_counter += 1
            return {"move": result["move"]}
        next_move = result

        self.turn_counter += 1
        return next_move

# TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
# board_width = game_state['board']['width']
# board_height = game_state['board']['height']


#x von 0 bis board_width -1
#y von 0 bis board_height -1
#Koordinaten zählen von 0, 
#während board_width und board_height von 1 zählen
    
# TODO: Step 2 - Prevent your Battlesnake from colliding with itself
# my_body = game_state['you']['body']

# TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
# opponents = game_state['board']['snakes']

# TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
# food = game_state['board']['food']
