
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
            self.is_move_safe["left"]["is_safe"] = False

        elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
            self.is_move_safe["right"]["is_safe"] = False

        elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
            self.is_move_safe["down"]["is_safe"] = False

        elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
            self.is_move_safe["up"]["is_safe"] = False         

       
        
    def not_wall_collision(self, game_state):

        my_head = game_state["you"]["head"]  
        
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

    def not_enemy_collision(self, game_state):
        
        my_position = game_state["you"]["head"]

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
            if opponent_length >= my_length:
                positions[snake["id"]]["unsafe"].extend(moves)
            else:
                positions[snake["id"]]["priority"].extend(moves)

            for i , body_part in enumerate(snake["body"]):

                if i != len(snake["body"]) - 1:
                    
                    positions[snake["id"]]["unsafe"].append(body_part)
                else:
                    if self.is_growing(snake, game_state):

                        positions[snake["id"]]["unsafe"].append(snake["body"][-1])

        return positions
    
    def reset_is_move_safe(self):

        for data in self.is_move_safe.values():

            data["is_safe"] = True

            data["priority"] = 0
    
    def choose_move(self, game_state):

        self.reset_is_move_safe()
        self.not_backward(game_state)
        self.not_wall_collision(game_state)
        self.not_itself_collision(game_state)
        self.not_enemy_collision(game_state)
        
        # Are there any safe moves left?
        safe_moves = {}
        for move , data in self.is_move_safe.items():

            if data["is_safe"] == True:

                safe_moves[move] = data["priority"]  

        if safe_moves == {}:
            turn = game_state.get("turn", "?")
            print(f"MOVE {turn}: No safe moves detected! Moving down")
            return {"move": "down"}
        
        # Choose a random move from the safe ones 
        memory_moves = []
        memory_priority = 0
        
        for move , priority in safe_moves.items():

            if memory_moves == [] and memory_priority == 0:

                if priority != 0:
                
                    memory_moves.append(move)
                    memory_priority = priority

            if memory_priority != 0:
            
                if priority > memory_priority:

                    memory_moves.clear()
                    memory_moves.append(move)
                    memory_priority = priority

                if priority == memory_priority:

                    memory_moves.append(move)
        
        if memory_moves != []:

            next_move = random.choice(memory_moves)

            return {"move": next_move}
        else:
            next_move = random.choice(list(safe_moves.keys()))
            
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