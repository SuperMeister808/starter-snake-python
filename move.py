
import random

class Move():

    def __init__(self):

        self.is_move_safe = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}

    def not_backward(self, game_state):

        # We've included code to prevent your Battlesnake from moving backwards
        my_head = game_state["you"]["body"][0]  # Coordinates of your head
        my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

        if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
            self.is_move_safe["left"] = False

        elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
            self.is_move_safe["right"] = False

        elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
            self.is_move_safe["down"] = False

        elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
            self.is_move_safe["up"] = False         

       
        
    def not_wall_collision(self, game_state):

        my_head = game_state["you"]["body"][0]  # Coordinates of your head
        my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
        
        board_width = game_state["board"]["width"]
        board_hight = game_state["board"]["height"]
    
        if my_head["x"] == board_width -1:

            self.is_move_safe["right"]["is_safe"] = False

        if my_head["x"] == 0:

            self.is_move_safe["left"]["is_safe"] = False

        if my_head["y"] == board_hight -1:

            self.is_move_safe["up"]["is_safe"] = False

        if my_head["y"] == 0:

            self.is_move_safe["down"]["is_safe"] = False

    def not_itself_collision(self, game_state):

        my_body = game_state["you"]["body"]

        position = game_state["you"]["head"]

        position_x = position["x"]

        position_y = position["y"]
        
        for e in my_body:

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

    def not_enemy_collision(self, game_state):
        
        my_position = game_state["you"]["head"]

        first_move = {"x": my_position["x"] + 1, "y": my_position["y"]}

        second_move = {"x": my_position["x"] - 1, "y": my_position["y"]}

        third_move = {"x": my_position["x"], "y": my_position["y"] + 1}

        fourth_move = {"x": my_position["x"], "y": my_position["y"] - 1}

        opponents_positions = self.calculate_opponents_positions(game_state)

        for snake in opponents_positions:
                
            for entry in snake["unsafe"]:
            
                if entry == first_move:

                    self.is_move_safe["right"]["is_safe"] = False

                if entry == second_move:

                    self.is_move_safe["left"]["is_safe"] = False

                if entry == third_move:

                    self.is_move_safe["up"]["is_safe"] = False

                if entry == fourth_move:

                    self.is_move_safe["down"]["is_safe"] = False

            for entry in snake["priority"]:

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

        positions = []
        
        snakes = game_state["board"]["snakes"]

        my_length = game_state["you"]["length"]
        
        i = 0
        
        for snake in snakes:

            if snake["id"] != game_state["you"]["id"]:
                
                body = snake["body"]

                head = snake["head"]

                body_parts = body[1:-1]

                tail = body[-1]

                opponent_length = snake["length"]

                positions.append({snake["id"]: {"unsafe": [], "priority": []}})
                
                positions[i][snake["id"]]["unsafe"].append(head)
                
                if opponent_length >= my_length:
                    
                    first_move = {"x": head["x"] + 1, "y": head["y"]}

                    positions[snake["id"]]["unsafe"].append(first_move)

                    second_move = {"x": head["x"] - 1, "y": head["y"]}

                    positions[snake["id"]]["unsafe"].append(second_move)

                    third_move = {"x": head["x"], "y": head["y"] + 1}

                    positions[snake["id"]]["unsafe"].append(third_move)

                    fourth_move = {"x": head["x"], "y": head["y"] - 1}

                    positions[snake["id"]]["unsafe"].append(fourth_move)
                else:
                    positions[i][snake["id"]]["priority"].append(first_move)

                    positions[i][snake["id"]]["priority"].append(second_move)

                    positions[i][snake["id"]]["priority"].append(third_move)

                    positions[i][snake["id"]]["priority"].append(fourth_move)

                for body_part in body_parts:

                    positions.append(body_part)

                if self.is_growing(snake, game_state):

                    positions.append(tail)

                i += 1

        return positions
    
    def choose_move(self, game_state):

        self.not_backward(game_state)
        self.not_wall_collision(game_state)
        self.not_itself_collision(game_state)
        self.not_enemy_collision(game_state)
        
        # Are there any safe moves left?
        safe_moves = []
        for move in self.is_move_safe:

            key = move.keys()

            data = move[key]

            if data["is_safe"] == True:

                safe_moves.append({"move": key, "priority": data["priority"]})  

        if len(safe_moves) == 0:
            print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
            return {"move": "down"}
        
        # Choose a random move from the safe ones 
        memory_move = None
        memory_priority = None
        
        for move in safe_moves:

            if memory_move == None and memory_priority == None:

                if move["priority"] != 0:
                
                    memory_move = move["move"]
                    memory_priority = move["priority"]

            if move["priority"] > memory_priority:

                memory_move = move["move"]
                memory_priority = move["priority"]
        
        if memory_move is not None:

            next_move = memory_move
        else:
            next_move = random.choice(safe_moves)

        print(f"MOVE {game_state['turn']}: {next_move}")
        return {"move": next_move}

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