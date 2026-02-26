
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
            
            NEEDED_KEYWORDS = ["head", "game_state", "body", "neck"]

            if relevant_positions is None:
                head, game_state, body, neck = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)
                data = {"head": head, "body": body, "neck": neck}
                root_id = self.create_future_safety_tree(data)
                
                move_left = {"x": head["x"] - 1, "y": head["y"]}
                move_right = {"x": head["x"] + 1, "y": head["y"]}
                move_up = {"x": head["x"], "y": head["y"] + 1}
                move_down = {"x": head["x"], "y": head["y"] - 1}
                
                positions = {"id": root_id, "positions": [move_left, move_right, move_up, move_down]}
                relevant_positions = []
                relevant_positions.append(positions)

            safe_move_left = False
            for e in relevant_positions:
                pass

            return safe_move_left , new_relevant_positions , new_body , new_neck
    
    def create_future_safety_tree(self, data):

        self.future_safety_tree = FutureSafetyTree(data)
        root = self.future_safety_tree.root

        return root["id"]
    
    def call_future_safety(self, **kwargs):

            NEEDED_KEYWORDS = ["game_state", "body", "move", "calls", "head"]

            game_state , body , move , calls , head = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

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

                safe_move_left , relevant_position , new_body , new_neck = self.future_safety(relevant_position, head=head, game_state=game_state, body=new_body, neck=new_neck)

                if safe_move_left == False:
                    return False
                
            return True
    
    def reset_safe_moves(self):
         
        self.safe_moves = {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}