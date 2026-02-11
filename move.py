
import random

from git import Repo

import threading

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


    def not_backward(self, **kwargs):

        # We've included code to prevent your Battlesnake from moving backwards
        if "head" not in kwargs:
            raise RuntimeError("Key Word Arg fehlt!")
        my_head = kwargs["head"]  # Coordinates of your head
        if "neck" not in kwargs:
            raise RuntimeError("Key Word Arg fehlt!")
        my_neck = kwargs["neck"]  # Coordinates of your "neck"

        if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
            self.is_move_safe["left"]["is_safe"] = False

        elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
            self.is_move_safe["right"]["is_safe"] = False

        elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
            self.is_move_safe["down"]["is_safe"] = False

        elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
            self.is_move_safe["up"]["is_safe"] = False         

       
    def not_wall_collision(self, **kwargs):

        if "head" not in kwargs:
            raise RuntimeError("Key Word Arg fehlt!")
        my_head = kwargs["head"]
        if "game_state" not in kwargs:
            raise RuntimeError("Key Word Arg fehlt!")
        board_width = kwargs["game_state"]["board"]["width"]
        board_hight = kwargs["game_state"]["board"]["height"]
    
        if my_head["x"] == board_width -1:

            self.is_move_safe["right"]["is_safe"] = False

        if my_head["x"] == 0:

            self.is_move_safe["left"]["is_safe"] = False

        if my_head["y"] == board_hight -1:

            self.is_move_safe["up"]["is_safe"] = False

        if my_head["y"] == 0:

            self.is_move_safe["down"]["is_safe"] = False

    def not_itself_collision(self, **kwargs):

        if "body" not in kwargs:
            raise RuntimeError("Key Word Arg fehlt!")
        my_body = kwargs["body"]

        if "head" not in kwargs:
            raise RuntimeError("Key Word Arg fehlt!")
        position = kwargs["head"]

        position_x = position["x"]

        position_y = position["y"]
        
        for e in my_body[1:]:

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
        
        if "head" not in kwargs:
            raise RuntimeError("Key Word Arg fehlt!")
        my_position = kwargs["head"]
        if "game_state" not in kwargs:
            raise RuntimeError("Key Word Arg fehlt!")
        game_state = kwargs["game_state"]

        first_move = {"x": my_position["x"] + 1, "y": my_position["y"]}

        second_move = {"x": my_position["x"] - 1, "y": my_position["y"]}

        third_move = {"x": my_position["x"], "y": my_position["y"] + 1}

        fourth_move = {"x": my_position["x"], "y": my_position["y"] - 1}

        opponents_positions = self.calculate_opponents_positions(game_state)

        for snake , position in opponents_positions.items():
                
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

    def is_growing(self, snake, game_state):

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

    def calculate_opponents_positions(self, game_state):

        positions = {}
        
        snakes = game_state["board"]["snakes"]
        
        for snake in snakes:

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
                    if self.is_growing(snake, game_state):

                        positions[snake["id"]]["unsafe"].append(snake["body"][-1])

        return positions
    
    def calculate_food(self, **kwargs):

        if "head" not in kwargs:
            raise RuntimeError("Key Word Arg fehlt!")
        head = kwargs["head"]
        if "game_state" not in kwargs:
            raise RuntimeError("Key Word Arg fehlt!")
        game_state = kwargs["game_state"]
        
        food = game_state["board"]["food"]

        left_move = {"x": head["x"] - 1, "y": head["y"]}
        right_move = {"x": head["x"] + 1, "y": head["y"]}
        up_move = {"x": head["x"], "y": head["y"] + 1}
        down_move = {"x": head["x"], "y": head["y"] - 1}

        for item in food:
        
            if left_move["x"] == item["x"] and left_move["y"] == item["y"]:

                self.is_move_safe["left"]["priority"] += 1

            if right_move["x"] == item["x"] and right_move["y"] == item["y"]:

                self.is_move_safe["right"]["priority"] += 1

            if up_move["x"] == item["x"] and up_move["y"] == item["y"]:

                self.is_move_safe["up"]["priority"] += 1

            if down_move["x"] == item["x"] and down_move["y"] == item["y"]:

                self.is_move_safe["down"]["priority"] += 1
    
    def reset_is_move_safe(self):

        for data in self.is_move_safe.values():

            data["is_safe"] = True

            data["priority"] = 0

    def reset_is_move_safe_memory(self):

        for data in self.is_move_safe_memory.values():

            data["is_safe"] = True
            data["priority"] = 0
    
    def calculate_food(self, **kwargs):
        
        if "head" not in kwargs:
            raise RuntimeError("Key Word Arg fehlt!")
        head = kwargs["head"]
        if "game_state" not in kwargs:
            raise RuntimeError("Key Word Arg fehlt!")
        game_state = kwargs["game_state"]
        
        food_list = game_state["board"]["food"]

        left_move = {"x": head["x"] -1, "y": head["y"]}
        right_move = {"x": head["x"] + 1, "y": head["y"]}
        up_move = {"x": head["x"], "y": head["y"] + 1}
        down_move = {"x": head["x"], "y": head["y"] - 1}

        for item in food_list:

            if left_move["x"] == item["x"] and left_move["y"] == item["y"]:

                self.is_move_safe["left"]["priority"] += 1

            if right_move["x"] == item["x"] and left_move["y"] == item["y"]:

                self.is_move_safe["right"]["priority"] += 1

            if up_move["x"] == item["x"] and left_move["y"] == item["y"]:

                self.is_move_safe["up"]["priority"] += 1

            if down_move["x"] == item["x"] and left_move["y"] == item["y"]:

                self.is_move_safe["down"]["priority"] += 1

    def future_safety(self, game_state):

        opponent_positions = self.calculate_opponents_positions()
        safe_moves = []

        for move , data in self.is_move_safe.items():
            if data["is_safe"] == True:
                safe_moves.append(move)

        for move in safe_moves:

            current_position = game_state["you"]["head"]
            if move == "left":
                relevant_position = {"x": current_position["x"] -1, "y": current_position["y"]}
                neck = current_position
            if move == "right":
                relevant_position = {"x": current_position["x"] + 1, "y": current_position["y"]}
                neck = current_position
            if move == "up":
                relevant_position = {"x": current_position["x"], "y": current_position["y"] + 1}
                neck = current_position
            if move == "down":
                relevant_position = {"x": current_position["x"], "y": current_position["y"] - 1}
                neck = current_position
        
            self.check_moves(relevant_position, game_state, neck)

    def check_moves(self, head, game_state, body, neck):

        next_move = self.emergency_system(game_state, self.reset_is_move_safe)
        if next_move is not None:
            return next_move
        
        checks = [self.not_backward, 
                  self.not_wall_collision, 
                  self.not_itself_collision, 
                  self.not_enemy_collision, 
                  self.calculate_food]

        for check in checks:

            next_move = self.emergency_system(game_state, check, head=head,game_state=game_state, body=body, neck=neck)
            if next_move is not None:
                return next_move

    def safe_is_move_safe(self):

        self.is_move_safe_memory = self.is_move_safe

        self.reset_is_move_safe()

    def get_body(self, new_head, new_snake=None):
        
        if new_snake is None:
            new_snake = []

        new_snake.append(new_head)

        return new_snake
        
    def call_get_body(self, head, snake):
        
        new_snake = []
        
        for body_part in snake:
            
            new_snake = self.get_body(head, new_snake)

            head = body_part

        return new_snake



    
    def emergency_system(self, game_state, func, *args, **kwargs):

        emergency_moves = ["left", "right", "up", "down"]
        
        try: 
            func(*args, **kwargs)
        except Exception as e:
            EmergencyLogger.loger_queue.put((func.__name__, e, game_state))
            if func.__name__ == "reset_is_move_safe":
                self.is_move_safe = {"left": {"is_safe": True, "priority": 0}, 
                                 "right": {"is_safe": True, "priority": 0},
                                 "up": {"is_safe": True, "priority": 0},
                                 "down": {"is_safe": True, "priority": 0}}
                return None
            else:
                try:
                    next_move = random.choice(emergency_moves)
                    return {"move": next_move}
                except Exception as e:
                    EmergencyLogger.loger_queue.put((func.__name__, f"{e}", game_state))
                    return {"move": "down"}

    def get_safe_moves(self, game_state):

        # Are there any safe moves left?
        safe_moves = {}
        try:
            for move , data in self.is_move_safe.items():

                if data["is_safe"] == True:

                    safe_moves[move] = data["priority"]
            return safe_moves
        except Exception as e:
            EmergencyLogger.loger_queue.put(("safe_moves", f"{e}", game_state)) 
            safe_moves = {"left": 0, "right": 0, "up": 0, "down": 0} 
            return safe_moves
        
    def get_priority_moves(self, game_state, safe_moves):

        # Choose a random move from the safe ones 
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
            EmergencyLogger.loger_queue.put(("priority", f"{e}", game_state))
            memory_moves = []
            return memory_moves
        
    def random_choice(self, game_state, safe_moves, memory_moves):

        emergency_moves = ["left", "right", "up", "down"]
        
        try:
            next_move = random.choice(memory_moves)
            EmergencyLogger.loger_queue.put(("random_choice", "Success: Priority Move choosed", game_state))
            return {"move": next_move}
        except Exception as e:
            EmergencyLogger.loger_queue.put(("random_choice", f"No priorities set: {e}", game_state))
            try:
                keys = []
                for key , value in safe_moves.items():
                    keys.append(key)
                next_move = random.choice(keys)
                return {"move": next_move}
            except Exception as e:
                EmergencyLogger.loger_queue.put(("random_choice", f"No safe moves left: {e}", game_state))
                try:
                    next_move = random.choice(emergency_moves)
                    return {"move": next_move}
                except Exception as e:
                    EmergencyLogger.loger_queue.put(("random_choice", f"{e}", game_state))
                    return {"move": "down"}

    
    
    def choose_move(self, game_state):
        
        next_move = self.check_moves(game_state)
        if next_move is not None:
            return {"move": next_move}
        
        self.safe_is_move_safe()
        
        safe_moves = self.get_safe_moves(game_state)

        if safe_moves == {}:
            turn = game_state.get("turn", "?")
            print(f"MOVE {turn}: No safe moves detected! Moving down")
            return {"move": "down"}
        
        memory_moves = self.get_priority_moves(game_state, safe_moves)
        
        next_move = self.random_choice(game_state, safe_moves, memory_moves)
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