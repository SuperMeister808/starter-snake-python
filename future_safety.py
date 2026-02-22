
import typing

from keywords import Keywords
from move import Move

class FutureSafety():

    def __init__(self):
         
        self.keywords = Keywords()

        self.move = Move()

    def future_safety(self, relevant_position:typing.List[dict]=None, **kwargs):
            
            NEEDED_KEYWORDS = ["head", "game_state", "body", "neck"]

            head, game_state, body, neck = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

            
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
                
                self.move.reset_is_move_safe(**kwargs)

                result = self.move.check_moves(head=e, game_state=game_state, body=body, neck=neck)

                for move , data in self.move.is_move_safe.items():
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

            game_state , body , move , calls , head = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)


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