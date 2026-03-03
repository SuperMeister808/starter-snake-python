
import random

from git import Repo

import threading

import typing

from copy import deepcopy

from emergency_logger import EmergencyLogger
from keywords import Keywords
from emergency_system import EmergencySystem
from future_safety import FutureSafety

class Move():

    turn_counter = 0
    
    def __init__(self):
        
        self.is_move_safe = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}
        
        self.keywords = Keywords()
        
        self.emergency_system = EmergencySystem(self)

        self.future_safety = FutureSafety(self)

        self.opponents_positions = {}

        self.priority_moves = []


    def not_backward(self, is_move_safe, **kwargs):

        NEEDED_KEYWORDS = ["head", "neck"]

        head , neck = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

            
        if neck["x"] < head["x"]:  
            is_move_safe["left"]["is_safe"] = False

        elif neck["x"] > head["x"]:  
            is_move_safe["right"]["is_safe"] = False

        elif neck["y"] < head["y"]:  
            is_move_safe["down"]["is_safe"] = False

        elif neck["y"] > head["y"]: 
            is_move_safe["up"]["is_safe"] = False         
       
    def not_wall_collision(self, is_move_safe, **kwargs):

        NEEDED_KEYWORDS = ["head", "game_state"]

        head, game_state = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)


        board_width = game_state["board"]["width"]
        board_height = game_state["board"]["height"]
    
        if head["x"] == board_width -1:

            is_move_safe["right"]["is_safe"] = False

        if head["x"] == 0:

            is_move_safe["left"]["is_safe"] = False

        if head["y"] == board_height -1:

            is_move_safe["up"]["is_safe"] = False

        if head["y"] == 0:

            is_move_safe["down"]["is_safe"] = False

    def not_itself_collision(self, is_move_safe, **kwargs):

        NEEDED_KEYWORDS = ["head", "body"]
        

        head, body = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)


        position_x = head["x"]

        position_y = head["y"]
        
        for e in body[1:]:

            x = e["x"]
            y = e["y"]

            if (position_x) + 1 == x and position_y == y:

                is_move_safe["right"]["is_safe"] = False

            if (position_x) - 1 == x and position_y == y:

                is_move_safe["left"]["is_safe"] = False

            if (position_y) + 1 == y and position_x == x:

                is_move_safe["up"]["is_safe"] = False

            if (position_y) - 1 == y and position_x == x:

                is_move_safe["down"]["is_safe"] = False

    def not_enemy_collision(self, is_move_safe, **kwargs):
        
        NEEDED_KEYWORDS = ["head", "game_state"]

        head, game_state = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)


        first_move = {"x": head["x"] + 1, "y": head["y"]}

        second_move = {"x": head["x"] - 1, "y": head["y"]}

        third_move = {"x": head["x"], "y": head["y"] + 1}

        fourth_move = {"x": head["x"], "y": head["y"] - 1}

        for snake , position in self.opponents_positions.items():
                
            if snake != game_state["you"]["id"]:
            
                for entry in position["unsafe"]:
            
                    if entry == first_move:

                        is_move_safe["right"]["is_safe"] = False

                    if entry == second_move:

                        is_move_safe["left"]["is_safe"] = False

                    if entry == third_move:

                        is_move_safe["up"]["is_safe"] = False

                    if entry == fourth_move:

                        is_move_safe["down"]["is_safe"] = False

                for entry in position["priority"]:

                    if entry == first_move:

                        is_move_safe["right"]["priority"] += 2

                    if entry == second_move:

                        is_move_safe["left"]["priority"] += 2

                    if entry == third_move:

                        is_move_safe["up"]["priority"] += 2

                    if entry == fourth_move:

                        is_move_safe["down"]["priority"] += 2

    def is_growing(self, **kwargs):

        NEEDED_KEYWORDS = ["head", "game_state"]

        head , game_state = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

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
        
        NEEDED_KEYWORDS = ["game_state", "my_length"]

        game_state , my_length = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)
        self.future_safety.log_data("calculate_opponents_positions", {"process": "extract_kwargs", "game_state": game_state, "my_length": my_length})
        
        self.reset_opponents_positions()
        copy_opponent_positions = deepcopy(self.opponents_positions)
        self.future_safety.log_data("calculate_opponents_positions", {"process": "reset_calculate_opponents_positions", "opponent_positions": copy_opponent_positions})
        
        snakes = game_state["board"]["snakes"]
        you = game_state["you"]
        self.future_safety.log_data("calculate_opponents_positions", {"process": "get snakes + you", "snakes": snakes, "you": you})
        
        for snake in snakes:

            if not isinstance(snake, dict):
                continue

            required_snake_keys = ["id", "head", "length", "body"]
            if any(key not in snake for key in required_snake_keys):
                continue

            if you["id"] == snake["id"]:
                continue

            self.opponents_positions [snake["id"]] = {"unsafe": [],"priority": []}
            self.future_safety.log_data("calculate_opponents_positions", {"process": "add snake into positions", "positions": positions})
            self.opponents_positions [snake["id"]]["unsafe"].append(snake["head"])
            self.future_safety.log_data("calculate_opponents_positions", {"process": "for snake positions appends head", "head": snake["head"], "positions": positions})
                          
            first_move = {"x": snake["head"]["x"] + 1, "y": snake["head"]["y"]}
            second_move = {"x": snake["head"]["x"] - 1, "y": snake["head"]["y"]}
            third_move = {"x": snake["head"]["x"], "y": snake["head"]["y"] + 1}
            fourth_move = {"x": snake["head"]["x"], "y": snake["head"]["y"] - 1}      
            moves = [first_move, second_move, third_move, fourth_move]      

            self.opponents_positions[snake["id"]]["priority"].extend(moves)
            my_length = game_state["you"]["length"]
            opponent_length = snake["length"]
            if opponent_length >= my_length:
                self.opponents_positions [snake["id"]]["unsafe"].extend(moves)

            for i , body_part in enumerate(snake["body"]):

                if i == len(snake["body"]) - 1:
                    
                    if self.is_growing(snake=snake, game_state=game_state):

                        self.opponents_positions[snake["id"]]["unsafe"].append(snake["body"][-1])
                else:
                    self.opponents_positions[snake["id"]]["unsafe"].append(body_part)



    def calculate_food(self, is_move_safe, **kwargs):
        
        NEEDED_KEYWORDS = ["head", "game_state"]

        head, game_state = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        
        food_list = game_state["board"]["food"]

        left_move = {"x": head["x"] -1, "y": head["y"]}
        right_move = {"x": head["x"] + 1, "y": head["y"]}
        up_move = {"x": head["x"], "y": head["y"] + 1}
        down_move = {"x": head["x"], "y": head["y"] - 1}

        for item in food_list:

            if left_move["x"] == item["x"] and left_move["y"] == item["y"]:

                is_move_safe["left"]["priority"] += 1

            if right_move["x"] == item["x"] and right_move["y"] == item["y"]:

                is_move_safe["right"]["priority"] += 1

            if up_move["x"] == item["x"] and up_move["y"] == item["y"]:

                is_move_safe["up"]["priority"] += 1

            if down_move["x"] == item["x"] and down_move["y"] == item["y"]:

                is_move_safe["down"]["priority"] += 1

    def check_moves(self, is_move_safe, **kwargs):
        
        NEEDED_KEYWORDS = ["head", "game_state", "body", "neck", "my_length"]

        head, game_state, body, neck, my_length = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        result = self.emergency_system.emergency_system(self.calculate_opponents_positions, game_state=game_state, my_length=my_length)
        if self.emergency_system.is_emergency(result):
            return result

        checks = [
                  self.not_backward, 
                  self.not_wall_collision, 
                  self.not_itself_collision, 
                  self.not_enemy_collision, 
                  self.calculate_food]

        for check in checks:

            result = check(is_move_safe, head=head, game_state=game_state, body=body, neck=neck)
            if self.emergency_system.is_emergency(result):
                return result
            
    def reset_is_move_safe(self):
        
        self.is_move_safe = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}
        
    def reset_opponents_positions(self):

        self.opponents_positions = {}

    def reset_priority_moves(self):

        self.priority_moves = []
    
    def get_body(self, new_body:typing.List[dict]=None, **kwargs):
        
        NEEDED_KEYWORDS = ["head"]

        head, = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        if new_body is None:
            new_body = []

        new_body.append(head)

        return new_body
        
    def call_get_body(self, **kwargs):
        
        NEEDED_KEYWORDS = ["head", "body"]
        
        head, body = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

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

        body, = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        try:
            neck = body[1]
        except IndexError:
            try:
                neck = body[0]
            except IndexError:
                raise IndexError("Body ist leer")
        
        return neck
    
    def get_length(self, body):

        length = len(body)
        return length
    
    #Edge-Case: turn 0
    def edit_body(self, body):
        new_body = []
        for seg in body:
            if seg not in new_body:
                new_body.append(seg)
        return new_body
    
    def check_safe_moves(self, calls, **kwargs):

        NEEDED_KEYWORDS = ["head", "game_state", "body", "neck", "my_length"]
        head , game_state , body , neck , my_length = self.emergency_system.emergency_system(self.keywords.extract_keywords, NEEDED_KEYWORDS, **kwargs)

        if calls < 1:
            raise RuntimeError("Mindestens 1 call erforderlich!")
        
        try:
            while calls > 0:
                copy = deepcopy(self.is_move_safe)
                for move , data in self.is_move_safe.items():
                    if data["is_safe"] == True:
                        result = self.emergency_system.emergency_system(self.future_safety.call_future_safety, calls, game_state=game_state, body=body, move=move, head=head, my_length=my_length, neck=neck)
                        if self.emergency_system.is_emergency(result):
                            return result
                        if result == False:
                            copy[move]["is_safe"] = False
                if any(data["is_safe"] == True for move , data in copy.items()):
                    break
                else:
                    calls = calls - 1
                
            self.is_move_safe = copy        
        except Exception as e:
            EmergencyLogger.loger_queue.put(("get_safe_moves", f"{e}", self.turn_counter, 40))
            self.reset_is_move_safe()
    
    def check_priority_moves(self):

        self.reset_priority_moves()
        
        try:
            priority_counter = 0
            for move , data in self.is_move_safe.items():
                if data["priority"] >  priority_counter:
                    self.priority_moves.clear()
                    self.priority_moves.append(move)
                    priority_counter = data["priority"]
                if data["priority"] == priority_counter and data["priority"] > 0:
                    self.priority_moves.append(move)
        except Exception as e:
            EmergencyLogger.loger_queue.put(("get_priority_moves", f"{e}", self.turn_counter, 40))
            self.priority_moves = []

    def random_choice(self):

        safe_opperturnities = []
        priority_opperturnities = []
        EMERGENCY_MOVES = ["left", "right", "up", "down"]
        try:
            for move , data in self.is_move_safe.items():
                if data["is_safe"] == True:
                    safe_opperturnities.append(move)
            for move in safe_opperturnities:
                if move in self.priority_moves:
                    priority_opperturnities.append(move)
            if len(priority_opperturnities) > 0:
                next_move = random.choice(priority_opperturnities)
                EmergencyLogger.loger_queue.put(("random_choice", "Successfully choosed priority move", self.turn_counter, 20))
                return {"move": next_move}
            if len(safe_opperturnities) > 0:
                next_move = random.choice(safe_opperturnities)
                EmergencyLogger.loger_queue.put(("random_choice", "Successfully choosed safe move", self.turn_counter, 20))
                return {"move": next_move}
            next_move = random.choice(EMERGENCY_MOVES)
            EmergencyLogger.loger_queue.put(("random_choice", "Choosed emergency move", self.turn_counter, 40))
            return {"move": next_move}
        except Exception as e:
            EmergencyLogger.loger_queue.put(("random_choice", f"{e}", self.turn_counter, 40))
            next_move = random.choice(EMERGENCY_MOVES)
            return {"move": next_move}
    
    def choose_move(self, game_state:typing.Dict):
         
        self.reset_is_move_safe()
        
        self.future_safety.log_data("choose_move", {"game_state": game_state})

        try:
            head = game_state["you"]["head"]
            raw_body = game_state["you"]["body"]
            body = self.edit_body(raw_body)
            my_length = game_state["you"]["length"]
            self.future_safety.log_data("choose_move", {"head": head, "body": body, "my_length": my_length})
        except Exception:
            raise RuntimeError("Variabele game_state nicht vorhanden!")
        
        result = self.emergency_system.emergency_system(self.get_neck, body=body, game_state=game_state)
        if self.emergency_system.is_emergency(result):
            Move.turn_counter += 1
            return {"move": result["move"]}
        neck = result
        self.future_safety.log_data("choose_move", {"head": head, "neck": neck, "body": body, "my_length": my_length})
        
        result = self.emergency_system.emergency_system(self.check_moves, self.is_move_safe, head=head, game_state=game_state, body=body, neck=neck, my_length=my_length)
        if self.emergency_system.is_emergency(result):
            Move.turn_counter += 1
            return {"move": result["move"]}
        self.future_safety.log_data("choose_move", {"head": head, "neck": neck, "body": body, "my_length": my_length})

        result = self.check_safe_moves(2, head=head, game_state=game_state, body=body, neck=neck, my_length=my_length)
        if self.emergency_system.is_emergency(result):
            Move.turn_counter += 1
            return {"move": result["move"]}
        self.future_safety.log_data("choose_move", {"head": head, "neck": neck, "body": body, "my_length": my_length})
        self.check_priority_moves()
        
        next_move = self.random_choice()
        Move.turn_counter += 1
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
