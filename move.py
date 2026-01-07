
import random

class Move():

    def __init__(self):

        self.is_move_safe = {"up": True, "down": True, "left": True, "right": True}

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

            self.is_move_safe["right"] = False

        if my_head["x"] == 0:

            self.is_move_safe["left"] = False

        if my_head["y"] == board_hight -1:

            self.is_move_safe["up"] = False

        if my_head["y"] == 0:

            self.is_move_safe["down"] = False    

    def not_itself_collision(self, game_state):

        my_body = game_state["you"]["body"]

    def choose_move(self, game_state):

        self.not_backward(game_state)
        self.not_wall_collision(game_state)
        self.not_itself_collision(game_state)
        
        # Are there any safe moves left?
        safe_moves = []
        for move, isSafe in self.is_move_safe.items():
            if isSafe:
                safe_moves.append(move)

        if len(safe_moves) == 0:
            print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
            return {"move": "down"}
        
        # Choose a random move from the safe ones
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