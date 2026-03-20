
import typing
from copy import deepcopy

from keywords import Keywords
from logger.emergency_logger import EmergencyLogger
from emergency_system import EmergencySystem
from future.future_safety_tree import FutureSafetyTree

class FutureSafety():

    def __init__(self, move):
         
        self.move = move
        self.keywords = Keywords()
        self.emergency_system = EmergencySystem(self.move)
        self.future_safety_tree = FutureSafetyTree()

        self.safe_moves = {"left": {"is_safe": True, "priority": 0}, "right": {"is_safe": True, "priority": 0}, "up": {"is_safe": True, "priority": 0}, "down": {"is_safe": True, "priority": 0}}
        
        self.tree_id = [0]

    # Simulates all safe future moves from the current position by building a tree.
    # Returns whether any safe move exists and the list of leaf node ids.
    def future_safety(self, node_ids=None, **kwargs):

        NEEDED_KEYWORDS = ["head", "game_state", "body", "neck", "my_length"]
        head, game_state, body, neck, my_length = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        # initialize tree with current position as root
        if node_ids is None:
            data = {"head": head, "body": body, "neck": neck, "my_length": my_length}
            root_id = self.create_future_safety_tree(data)
            node_ids = [root_id]

        safe_move_left = False

        for node_id in node_ids[:]:

            self.reset_safe_moves()
            head, body, neck, my_length = self.extract_data_from_tree(node_id)
            self.move.check_moves(self.safe_moves, head=head, game_state=game_state, body=body, neck=neck, my_length=my_length)

            for move, data in self.safe_moves.items():
                if not data["is_safe"]:
                    continue

                safe_move_left = True
                new_body = body.copy()
                move_position = self.get_move(move, head)

                # body calculation depends on whether the snake is growing
                if self.move.is_growing(head=move_position, game_state=game_state):
                    new_body, new_neck, new_length = self.create_data_from_head_is_growing(move_position, new_body, my_length)
                else:
                    new_body, new_neck, new_length = self.create_data_from_head(move_position, new_body, my_length)

                data = {"head": move_position, "body": new_body, "neck": new_neck, "my_length": new_length}
                child_id = self.future_safety_tree.add_node(data, node_id)
                node_ids.append(child_id)

            node_ids.remove(node_id)

        return safe_move_left, node_ids
    
    # Extracts head, body, neck and length from a tree node by its id.
    def extract_data_from_tree(self, id):

        parent = self.future_safety_tree.find_parent(id)
        data = parent["data"]

        return data["head"], data["body"], data["neck"], data["my_length"]
    
    # Calculates the new body, neck and length after a move without growing.
    def create_data_from_head(self, head, body, length):
        new_body = self.move.call_get_body(head=head, body=body)
        new_neck = self.move.get_neck(body=new_body)
        return new_body, new_neck, length
    
    # Calculates the new body, neck and length after a move when the snake is growing.
    # Inserts the new head at the front and increments the length by 1.
    def create_data_from_head_is_growing(self, head, body, length):
        body.insert(0, head)
        new_neck = self.move.get_neck(body=body)
        return body, new_neck, length + 1
    
    # Returns all four possible next positions from the current head position.
    def create_moves(self, head):
        return (
            {"x": head["x"] - 1, "y": head["y"]},  # left
            {"x": head["x"] + 1, "y": head["y"]},  # right
            {"x": head["x"],     "y": head["y"] - 1},  # down
            {"x": head["x"],     "y": head["y"] + 1},  # up
        )
    
    # Returns the new head position for the given move direction.
    def get_move(self, move, head):
        moves = {
            "left":  {"x": head["x"] - 1, "y": head["y"]},
            "right": {"x": head["x"] + 1, "y": head["y"]},
            "down":  {"x": head["x"],     "y": head["y"] - 1},
            "up":    {"x": head["x"],     "y": head["y"] + 1},
        }
        return moves.get(move)
    
    # Initializes the future safety tree with the current game state as root.
    # Returns the root node id to use as the starting point for simulation.
    def create_future_safety_tree(self, data):
        self.future_safety_tree.create_root(data)
        return self.future_safety_tree.root["id"]
    
    # Simulates future turns for a given move to verify it remains safe.
    # Returns True if at least one safe path exists after all simulated turns.
    def call_future_safety(self, calls=None, **kwargs):

        if calls is None:
            calls = 2

        NEEDED_KEYWORDS = ["game_state", "body", "move", "head", "my_length", "neck"]
        game_state, body, move, head, my_length, neck = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        # calculate the new head position and body for the move being simulated
        head = self.get_move(move, head)
        new_body = self.move.call_get_body(body=body, head=head)
        new_neck = self.move.get_neck(body=new_body)

        # simulate future turns and track whether any safe path remains
        node_ids = None
        for i in range(calls):
            safe_move_left, node_ids = self.future_safety(
                node_ids, head=head, game_state=game_state,
                body=new_body, neck=new_neck, my_length=my_length
            )

        return safe_move_left
    
    # Attempts future safety simulation with decreasing number of turns.
    # Reduces calls by 1 each time no safe path is found.
    # Falls back to emergency move if simulation raises an exception.
    def fallback_future_safety(self, calls, game_state, body, move, head, my_length, neck):

        if calls < 1:
            raise RuntimeError("At least 1 call is required!")

        while calls > 0:
            result = self.emergency_system.emergency_system(
                self.call_future_safety, calls,
                game_state=game_state, body=body, move=move,
                head=head, my_length=my_length, neck=neck
            )

            if self.emergency_system.is_emergency(result):
                return result

            # treat non-bool results as unsafe
            if not isinstance(result, bool):
                result = False

            if result:
                return result

            calls -= 1

        return result

    # Logs debug data to the async logger queue with level 10 (DEBUG).
    def log_data(self, where, data):
        EmergencyLogger.loger_queue.put((where, data, self.move.turn_counter, 10))
    
    # Resets all moves to safe with zero priority before simulating each node.
    def reset_safe_moves(self):
        self.safe_moves = {
            "left":  {"is_safe": True, "priority": 0},
            "right": {"is_safe": True, "priority": 0},
            "up":    {"is_safe": True, "priority": 0},
            "down":  {"is_safe": True, "priority": 0},
        }
