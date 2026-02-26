
import typing

from keywords import Keywords
from future_safety_tree import FutureSafetyTree

class FutureSafety():

    def __init__(self, move):
         
        self.keywords = Keywords()

        self.move = move

        self.safe_moves = {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}

        self.tree_id = [0]

    def future_safety(self, relevant_position:typing.List[dict], **kwargs):
            
            NEEDED_KEYWORDS = ["head", "game_state", "body", "neck"]

            head, game_state, body, neck = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)
            tree_data = {"head": head, "body": body, "neck": neck}
            future_safety_tree = FutureSafetyTree(tree_data)
            
            if relevant_position == []:
                
                move_left = {"x": head["x"] - 1, "y": head["y"]}
                move_right = {"x": head["x"] + 1, "y": head["y"]}
                move_up = {"x": head["x"], "y": head["y"] + 1}
                move_down = {"x": head["x"], "y": head["y"] - 1}
                possible_moves = [move_left, move_right, move_up, move_down]
            
                relevant_position.extend(possible_moves)

            safe_move_left = False
            new_relevant_positions = []
            
            try:
                for e in relevant_position:
                
                    self.reset_safe_moves()
                    new_body = self.move.call_get_body(head=e, body=body)
                    new_neck = self.move.get_neck(body=new_body)
                    
                    result = self.move.check_moves(self.safe_moves, head=e, game_state=game_state, body=new_body, neck=new_neck)


                    for move , data in self.safe_moves.items():
                        if data["is_safe"] == True:
                            safe_move_left = True
                
                        
                            move_left = {"x": e["x"] - 1, "y": e["y"]}
                            move_right = {"x": e["x"] + 1, "y": e["y"]}
                            move_up = {"x": e["x"], "y": e["y"] + 1}
                            move_down = {"x": e["x"], "y": e["y"] - 1}
                            possible_moves = [move_left, move_right, move_up, move_down]
                        

                            new_relevant_positions.extend(possible_moves)
            except TypeError:
                raise TypeError("relevant_position muss als Liste übergeben werden")
            
            return safe_move_left , new_relevant_positions , new_body , new_neck
    
    def future_safety_tree_add_node(self, data, parent):

        
    
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

            body = self.move.call_get_body(body=body, head=head)

            relevant_position = []
            new_body = self.move.call_get_body(body=body, head=head)
            new_neck = self.move.get_neck(body=new_body)
            for i in range(calls):

                safe_move_left , relevant_position , new_body , new_neck = self.future_safety(relevant_position, head=head, game_state=game_state, body=new_body, neck=new_neck)

                if safe_move_left == False:
                    return False
                
            return True
    
    def reset_safe_moves(self):
         
        self.safe_moves = {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}