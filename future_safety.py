
import typing
from copy import deepcopy

from keywords import Keywords
from emergency_logger import EmergencyLogger
from emergency_system import EmergencySystem
from future_safety_tree import FutureSafetyTree

class FutureSafety():

    def __init__(self, move):
         
        self.move = move
        self.keywords = Keywords()
        self.emergency_system = EmergencySystem(self.move)
        self.future_safety_tree = FutureSafetyTree()

        self.safe_moves = {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}
        
        self.tree_id = [0]

    def future_safety(self, node_ids=None, **kwargs):
            
            NEEDED_KEYWORDS = ["head", "game_state", "body", "neck", "my_length"]

            head, game_state, body, neck, my_length = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)
            if node_ids is None:
                data = {"head": head, "body": body, "neck": neck, "my_length": my_length}
                root_id = self.create_future_safety_tree(data)
                self.log_data("future_safety", {"process": "create root form args", "data": data})
                
                node_ids = []
                node_ids.append(root_id)
                self.log_data("future_safety", {"process": "added root into relevant_nodes"})

            safe_move_left = False
            for node_id in node_ids[:]:
                
                self.reset_safe_moves()
                
                head , body , neck , my_length = self.extract_data_from_tree(node_id)
                self.log_data("future_safety", {"process": "extract_data_from_tree", "head": head, "body": body, "neck": neck, "my_length": my_length})
                    
                self.move.check_moves(self.safe_moves, head=head, game_state=game_state, body=body, neck=neck, my_length=my_length)
                self.log_data("future_safety", {"process": "check_moves", "head": head, "body": body, "neck": neck, "my_length": my_length})

                for move , data in self.safe_moves.items():
                    new_body = body.copy()
                    if data["is_safe"] == True:
                        
                        safe_move_left = True
                        move_possition = self.get_move(move, head)
                        if self.move.is_growing(head=move_possition, game_state=game_state):
                            new_body, new_neck , new_length = self.create_data_from__head_is_growing(move_possition, new_body, my_length)
                        else:
                            new_body , new_neck , new_length = self.create_data_from_head(move_possition, new_body, my_length)
                        data = {"head": move_possition, "body": new_body, "neck": new_neck, "my_length": new_length}
                        child_id = self.future_safety_tree.add_node(data, node_id)
                        node_ids.append(child_id)
                        self.log_data("future_safety", {"process": "add_node_safe_move", "head": move_possition, "body": new_body, "neck": new_neck, "my_length": new_length})

                node_ids.remove(node_id)
                self.log_data("future_safety", {"process": "remove_current_node"})

            return safe_move_left , node_ids
    
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

        self.future_safety_tree.create_root(data)
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
            node_ids = None
            for i in range(calls):
                safe_move_left , node_ids = self.future_safety(node_ids, head=head, game_state=game_state, body=new_body, neck=new_neck, my_length=my_length)

            if safe_move_left == False:
                return False
                
            return True
    
    def fallback_future_safety(self, calls, game_state, body, move, head, my_length, neck):

        if calls < 1:
            raise RuntimeError("Mindestens 1 call erforderlich!")
        
        while calls > 0:
            result = self.emergency_system.emergency_system(self.call_future_safety, calls, game_state=game_state, body=body, move=move, head=head, my_length=my_length, neck=neck)
            if self.emergency_system.is_emergency(result):
                return result
            if not isinstance(result, bool):
                result = False
            if result == True:
                return result
            if result == False:
                calls = calls - 1

        return result

    def log_data(self, where, data):

        EmergencyLogger.loger_queue.put((where, data, self.move.turn_counter, 10))
    
    def reset_safe_moves(self):
         
        self.safe_moves = {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}