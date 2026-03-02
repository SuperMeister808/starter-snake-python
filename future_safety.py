
import typing

from keywords import Keywords
from emergency_logger import EmergencyLogger
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
                self.log_data("future_safety", {"process": "create root form args", "data": data})
                
                positions = {"id": root_id}
                relevant_positions = []
                relevant_positions.append(positions)
                self.log_data("future_safety", {"process": "added root into relevant_position"})

            safe_move_left = False
            for e in relevant_positions[:]:
                
                self.reset_safe_moves()
                
                id = e["id"]
                head , body , neck , length = self.extract_data_from_tree(id)
                self.log_data("future_safety", {"process": "extract_data_from_tree", "head": head, "body": body, "neck": neck, "my_length": my_length})
                    
                self.move.check_moves(self.safe_moves, head=head, game_state=game_state, body=body, neck=neck, my_length=length)
                self.log_data("future_safety", {"process": "check_moves", "head": head, "body": body, "neck": neck, "my_length": length})

                for move , data in self.safe_moves.items():
                    if data["is_safe"] == True:
                        safe_move_left = True
                        move_possition = self.get_move(move, head)
                        new_body , new_neck , new_length = self.create_data_from_head(move_possition, body, length)
                        data = {"head": move_possition, "body": new_body, "neck": new_neck, "my_length": new_length}
                        child_id = self.future_safety_tree.add_node(data, id)
                        relevant_positions.append(child_id)
                        self.log_data("future_safety", {"process": "add_node_safe_move", "head": move_possition, "body": new_body, "neck": new_neck, "my_length": my_length})

                relevant_positions.remove(e)
                self.log_data("future_safety", {"process": "remove_current_node"})

            return safe_move_left , relevant_positions
    
    def extract_data_from_tree(self, id):
         
        parent = self.future_safety_tree.find_parent(id)
        data = parent["data"]
        
        head = data["head"]
        body = data["body"]
        neck = data["neck"]
        my_length = data["my_length"]

        return head , body , neck , my_length
    
    def create_data_from_head(self, head, body, length):

        new_body = self.move.call_get_body(head=head, body=body)
        new_neck = self.move.get_neck(body=new_body)
        my_length = length
        return new_body , new_neck , my_length
    
    def create_data_from__head_is_growing(self, head, body, length):
        
        body.insert(0, head)
        new_neck = self.move.get_neck(body=body)
        new_length = length + 1
        return body , new_neck , new_length
    
    def create_moves(self, head):
         
        move_left = {"x": head["x"] - 1, "y": head["y"]}
        move_right = {"x": head["x"] + 1, "y": head["y"]}
        move_down = {"x": head["x"], "y": head["y"] - 1}
        move_up = {"x": head["x"], "y": head["y"] + 1}

        return move_left , move_right , move_down , move_up
    
    def get_move(self, move, head):

        move_left , move_right , move_down , move_up = self.create_moves(head)
        if move == "left":
            return move_left
        if move == "right":
            return move_right
        if move == "down":
            return move_down
        if move == "up":
            return move_up
    
    def create_future_safety_tree(self, data):

        self.future_safety_tree = FutureSafetyTree(data)
        root = self.future_safety_tree.root

        return root["id"]
    
    def call_future_safety(self, calls=None, **kwargs):

            if calls is None:
                calls = 2
            
            NEEDED_KEYWORDS = ["game_state", "body", "move", "head", "my_length", "neck"]

            game_state , body , move , head , my_length, neck = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)
            self.log_data("call_future_safety", {"process": "get_kwargs", "body": body, "move": move, "head": head, "my_length": my_length, "neck": neck})

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

            self.log_data("call_future_safety", {"process": "calculate body for move which will be simulated", "body": new_body, "neck": new_neck, "head": head, "my_length": my_length})
            relevant_position = None
            for i in range(calls):
                safe_move_left , relevant_position = self.future_safety(relevant_position, head=head, game_state=game_state, body=new_body, neck=new_neck, my_length=my_length)

            if safe_move_left == False:
                return False
                
            return True
    
    def log_data(self, where, data):

        EmergencyLogger.loger_queue.put((where, data, self.move.turn_counter, 10))
    
    def reset_safe_moves(self):
         
        self.safe_moves = {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}