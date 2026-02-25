
import random

from git import Repo

import threading

import typing

import copy

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

                        is_move_safe["right"]["priority"] += 1

                    if entry == second_move:

                        is_move_safe["left"]["priority"] += 1

                    if entry == third_move:

                        is_move_safe["up"]["priority"] += 1

                    if entry == fourth_move:

                        is_move_safe["down"]["priority"] += 1

    def is_growing(self, **kwargs):

        NEEDED_KEYWORDS = ["snake", "game_state"]

        snake , game_state = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)


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

        game_state, = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        
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
        
        NEEDED_KEYWORDS = ["head", "game_state", "body", "neck"]

        head, game_state, body, neck = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)


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
    
    def check_safe_moves(self, **kwargs):

        NEEDED_KEYWORDS = ["head", "game_state", "body", "neck"]
        head , game_state , body , neck = self.emergency_system.emergency_system(self.keywords.extract_keywords, NEEDED_KEYWORDS, **kwargs)

        try:
            for move , data in self.is_move_safe.items():
                if data["is_safe"] == True:
                    result = self.emergency_system.emergency_system(self.future_safety.call_future_safety, calls=2, move=move, head=head, game_state=game_state, body=body, neck=neck)
                    if self.emergency_system.is_emergency(result):
                        Move.turn_counter += 1
                        return {"move": result["move"]}
                    if result == False:
                        self.is_move_safe[move]["is_safe"] = False
        except Exception as e:
            EmergencyLogger.loger_queue.put(("get_safe_moves", f"{e}", self.turn_counter))
            self.reset_is_move_safe()

    def check_priority_moves(self):

        try:
            priority_counter = 0
            for move , data in self.is_move_safe.items():
                if data["priority"] >  priority_counter:
                    self.priority_moves.clear()
                    self.priority_moves.append(move)
                    priority_counter = data["priority"]
                if data["priority"] == priority_counter:
                    self.priority_moves.append(move)
        except Exception as e:
            EmergencyLogger.loger_queue.put(("get_priority_moves", f"{e}", self.turn_counter))
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
                EmergencyLogger.loger_queue.put(("random_choice", "Successfully choosed priority move", self.turn_counter))
                return {"move": next_move}
            if len(safe_opperturnities) > 0:
                next_move = random.choice(safe_opperturnities)
                EmergencyLogger.loger_queue.put(("random_choice", "Successfully choosed safe move", self.turn_counter))
                return {"move": next_move}
            next_move = random.choice(EMERGENCY_MOVES)
            EmergencyLogger.loger_queue.put(("random_choice", "Choosed emergency move", self.turn_counter))
            return {"move": next_move}
        except Exception as e:
            EmergencyLogger.loger_queue.put(("random_choice", f"{e}", self.turn_counter))
            next_move = random.choice(EMERGENCY_MOVES)
            return {"move": next_move}
    
    def choose_move(self, game_state:typing.Dict):
         
        self.reset_is_move_safe()
        
        try:
            head = game_state["you"]["head"]
            body = game_state["you"]["body"]
        except Exception:
            raise RuntimeError("Variabele game_state nicht vorhanden!")
        
        result = self.emergency_system.emergency_system(self.get_neck, body=body, game_state=game_state)
        if self.emergency_system.is_emergency(result):
            Move.turn_counter += 1
            return {"move": result["move"]}
        neck = result

        result = self.emergency_system.emergency_system(self.calculate_opponents_positions, game_state=game_state)
        if self.emergency_system.is_emergency(result):
            Move.turn_counter += 1
            return {"move": result["move"]}
        self.opponents_positions = result
        
        result = self.emergency_system.emergency_system(self.check_moves, self.is_move_safe, head=head, game_state=game_state, body=body, neck=neck)
        if self.emergency_system.is_emergency(result):
            Move.turn_counter += 1
            return {"move": result["move"]}

        self.check_safe_moves(head=head, game_state=game_state, body=body, neck=neck)
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
