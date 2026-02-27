
import typing

from keywords import Keywords
from future_safety_tree import FutureSafetyTree

class FutureSafety():

    def __init__(self, move):
         
        self.keywords = Keywords()

        self.move = move

        self.safe_moves = {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}
        
        self.tree_id = [0]

    def future_safety(self, relevant_positions=None, **kwargs):
            
            NEEDED_KEYWORDS = ["head", "game_state", "body", "neck", "my_length"]

            if relevant_positions is None:
                head, game_state, body, neck, my_length = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)
                data = {"head": head, "body": body, "neck": neck, "my_length": my_length}
                root_id = self.create_future_safety_tree(data)
                
                positions = {"id": root_id}
                relevant_positions = []
                relevant_positions.append(positions)

            safe_move_left = False
            for e in relevant_positions:
                
                self.reset_safe_moves()
                
                id = e["id"]
                head , body , neck , my_length = self.extract_data_from_tree(id)

                move_left , move_right , move_down , move_up = self.create_moves(head)
                possible_moves = [move_left, move_right, move_down, move_up]
                
                new_relevant_position = []
                for move in possible_moves:
                    
                    self.reset_safe_moves()
                    
                    snake = {"head": move}
                    if self.move.is_growing(snake=move, game_state=game_state) == True:
                        new_body , new_neck , new_length = self.create_data_from__head_is_growing(head, body)
                    else:
                        new_body , new_neck , my_length = self.create_data_from_head(move, body)

                    self.move.check_moves(self.safe_moves, head=move, game_state=game_state, body=new_body, neck=new_neck, my_length=my_length)
                    for move , data in self.safe_moves.items():
                        if data["is_safe"] == True:
                            safe_move_left = True
                            data = {"head": move, "body": new_body, "neck": new_neck, "my_length": my_length}
                            child_id = self.future_safety_tree.add_node(data, id)
                            new_relevant_position.append(child_id)

                relevant_positions.remove(e)
                relevant_positions.extend(new_relevant_position)
                new_relevant_position.clear()

            return safe_move_left , relevant_positions
    
    def extract_data_from_tree(self, id):
         
        parent = self.future_safety_tree.find_parent(id)
        data = parent["data"]
        
        head = data["head"]
        body = data["body"]
        neck = data["neck"]
        my_length = data["my_length"]

        return head , body , neck , my_length
    
    def create_data_from_head(self, head, body):

        new_body = self.move.call_get_body(head=head, body=body)
        new_neck = self.move.get_neck(body=new_body)
        my_length = self.move.get_length(body)
        return new_body , new_neck , my_length
    
    def create_data_from__head_is_growing(self, head, body):
        
        body.insert(0, head)
        new_neck = self.move.get_neck(body=body)
        new_length = self.move.get_length(body)
        return body , new_neck , new_length
    
    def create_moves(self, head):
         
        move_left = {"x": head["x"] - 1, "y": head["y"]}
        move_right = {"x": head["x"] + 1, "y": head["y"]}
        move_down = {"x": head["x"], "y": head["y"] - 1}
        move_up = {"x": head["x"], "y": head["y"] + 1}

        return move_left , move_right , move_down , move_up
    
    def create_future_safety_tree(self, data):

        self.future_safety_tree = FutureSafetyTree(data)
        root = self.future_safety_tree.root

        return root["id"]
    
    def call_future_safety(self, calls=None, **kwargs):

            if calls is None:
                calls = 2
            
            NEEDED_KEYWORDS = ["game_state", "body", "move", "head", "my_length"]

            game_state , body , move , head , my_length = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

            if move == "left":
                head = {"x": head["x"] -1, "y": head["y"]}
            if move == "right":
                head = {"x": head["x"] + 1, "y": head["y"]}
            if move == "up":
                head = {"x": head["x"], "y": head["y"] + 1}
            if move == "down":
                head = {"x": head["x"], "y": head["y"] - 1}
            new_body = self.move.call_get_body(body=body, head=head)
            new_neck = self.move.get_neck(body=new_body)

            relevant_position = None
            for i in range(calls):
                safe_move_left , relevant_position = self.future_safety(relevant_position, head=head, game_state=game_state, body=new_body, neck=new_neck, my_length=my_length)

            if safe_move_left == False:
                return False
                
            return True
    
    def reset_safe_moves(self):
         
        self.safe_moves = {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}