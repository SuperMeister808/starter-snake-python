
import random

from git import Repo

import threading

import typing

from copy import deepcopy

from logger.emergency_logger import EmergencyLogger
from keywords import Keywords
from emergency_system import EmergencySystem
from future.future_safety import FutureSafety
from extract_data import ExtractData

# Orchestrates the full move selection pipeline — evaluates safe and priority moves
# and returns the best available move each turn.
class Move():

    turn_counter = 0
    
    def __init__(self):
        
        self.is_move_safe = {"up": {"is_safe": True, "priority": 0}, 
                             "down": {"is_safe": True, "priority": 0}, 
                             "left": {"is_safe": True, "priority": 0}, 
                             "right": {"is_safe": True, "priority": 0}}
        
        self.keywords = Keywords()
        
        self.emergency_system = EmergencySystem(self)

        self.future_safety = FutureSafety(self)

        self.extract_data = ExtractData(self.keywords)

        self.opponents_positions = {}

        self.priority_moves = []

    # Marks the backward move as unsafe by comparing head and neck positions.
    def calculate_not_backward(self, is_move_safe, **kwargs):

        NEEDED_KEYWORDS = ["head", "neck"]
        head, neck = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        backward = self._get_backward_direction(head, neck)
    
        if backward:
            is_move_safe[backward]["is_safe"] = False

    # Determines the backward direction by comparing head and neck coordinates.
    def _get_backward_direction(self, head, neck):
        if neck["x"] < head["x"]: return "left"
        if neck["x"] > head["x"]: return "right"
        if neck["y"] < head["y"]: return "down"
        if neck["y"] > head["y"]: return "up"
        return None
       
    # Marks moves that would lead into a wall as unsafe.
    # Board coordinates run from 0 to width/height - 1.
    def calculate_not_wall_collision(self, is_move_safe, **kwargs):

        NEEDED_KEYWORDS = ["head", "game_state"]
        head, game_state = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        board_width = game_state["board"]["width"]
        board_height = game_state["board"]["height"]

        wall_collisions = self._get_wall_collisions(head, board_width, board_height)

        for direction in wall_collisions:
            is_move_safe[direction]["is_safe"] = False

    # Returns a list of directions that would result in a wall collision.
    def _get_wall_collisions(self, head, board_width, board_height):
        collisions = []
        if head["x"] >= board_width - 1:  collisions.append("right")
        if head["x"] <= 0:                collisions.append("left")
        if head["y"] >= board_height - 1: collisions.append("up")
        if head["y"] <= 0:                collisions.append("down")
        return collisions

    # Marks moves that would collide with the snake's own body as unsafe.
    # Skips the head (index 0) since the head is the current position.
    def calculate_not_itself_collision(self, is_move_safe, **kwargs):

        NEEDED_KEYWORDS = ["head", "body"]
        head, body = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        possible_moves = self._get_possible_moves(head)

        # skip index 0 since body[0] is the head itself
        for body_part in body[1:]:
            for direction, move in possible_moves.items():
                if move == body_part:
                    is_move_safe[direction]["is_safe"] = False

    # Marks moves that would collide with an opponent as unsafe.
    # Rewards moves that lead to a winning head-to-head position with priority + 2.
    def calculate_not_enemy_collision(self, is_move_safe, **kwargs):

        NEEDED_KEYWORDS = ["head", "game_state", "my_length"]
        head, game_state, my_length = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        if self.opponents_positions is None:
            self.calculate_opponents_positions(game_state, my_length)

        possible_moves = self._get_possible_moves(head)
        you_id = game_state["you"]["id"]

        for snake_id, position in self.opponents_positions.items():
            # skip yourself
            if snake_id == you_id:
                continue

            self._apply_unsafe_positions(is_move_safe, possible_moves, position["unsafe"])
            self._apply_priority_positions(is_move_safe, possible_moves, position["priority"])

    # Marks moves that overlap with opponent unsafe positions as unsafe.
    def _apply_unsafe_positions(self, is_move_safe, possible_moves, unsafe_positions):
        for direction, move in possible_moves.items():
            if move in unsafe_positions:
                is_move_safe[direction]["is_safe"] = False

    # Increases priority of moves that lead to a winning head-to-head position.
    # Priority + 2 rewards aggressive positioning against smaller opponents.
    def _apply_priority_positions(self, is_move_safe, possible_moves, priority_positions):
        for direction, move in possible_moves.items():
            if move in priority_positions:
                is_move_safe[direction]["priority"] += 2

    # Returns True if the snake is about to eat food on its next move.
    # Used to determine if the tail should be treated as unsafe.
    def calculate_is_growing(self, **kwargs):

        NEEDED_KEYWORDS = ["head", "game_state"]
        head, game_state = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        food = game_state["board"]["food"]
        possible_moves = self._get_possible_moves(head)

        return any(move in food for move in possible_moves.values())

    # Calculates unsafe and priority positions for all opponent snakes.
    # Unsafe positions block moves, priority positions reward head-to-head wins.
    def calculate_opponents_positions(self, **kwargs):
    
        NEEDED_KEYWORDS = ["game_state", "my_length"]
        game_state, my_length = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)
    
        # reset before recalculating to avoid stale positions from previous turn
        self.reset_opponents_positions()
    
        snakes = game_state["board"]["snakes"]
        you = game_state["you"]
    
        for snake in snakes:
            if not self._is_valid_opponent(snake, you):
                continue
        
            self.opponents_positions[snake["id"]] = {"unsafe": [], "priority": []}
        
            self._map_body_parts(snake, game_state)
            self._map_head_to_head_moves(snake, my_length)

    # Validates that a snake entry is a valid opponent and not yourself.
    def _is_valid_opponent(self, snake, you):
        if not isinstance(snake, dict):
            return False
        required_keys = ["id", "head", "length", "body"]
        if any(key not in snake for key in required_keys):
            return False
        if snake["id"] == you["id"]:
            return False
        return True

    # Maps each body part of an opponent to unsafe positions.
    # Head is always unsafe. Tail is only unsafe if the snake is growing.
    def _map_body_parts(self, snake, game_state):
        for i, body_part in enumerate(snake["body"]):
        
            # head is always unsafe
            if i == 0:
                self.opponents_positions[snake["id"]]["unsafe"].append(body_part)
                continue
        
            # tail is only unsafe if the snake ate food this turn
            if i == len(snake["body"]) - 1:
                if self.is_growing(head=snake["head"], game_state=game_state):
                    self.opponents_positions[snake["id"]]["unsafe"].append(body_part)
                continue
        
            # all other body parts are always unsafe
            self.opponents_positions[snake["id"]]["unsafe"].append(body_part)

    # Maps all possible next moves of an opponent to priority positions.
    # If the opponent is the same size or larger, their moves are also unsafe
    # since a head-to-head collision would be fatal.
    def _map_head_to_head_moves(self, snake, my_length):
        moves = [
            {"x": snake["head"]["x"] + 1, "y": snake["head"]["y"]},  # right
            {"x": snake["head"]["x"] - 1, "y": snake["head"]["y"]},  # left
            {"x": snake["head"]["x"], "y": snake["head"]["y"] + 1},  # up
            {"x": snake["head"]["x"], "y": snake["head"]["y"] - 1},  # down
        ]
    
        self.opponents_positions[snake["id"]]["priority"].extend(moves)
    
        # head-to-head is fatal if opponent is same size or larger
        if snake["length"] >= my_length:
            self.opponents_positions[snake["id"]]["unsafe"].extend(moves)

    # Increases priority of moves that lead directly to a food item.
    def calculate_food(self, is_move_safe, **kwargs):
    
        NEEDED_KEYWORDS = ["head", "game_state"]
        head, game_state = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)
    
        food_list = game_state["board"]["food"]
        moves = self._get_possible_moves(head)

        for food in food_list:
            for direction, move in moves.items():
                if move == food:
                    is_move_safe[direction]["priority"] += 1

    # Returns all four possible next positions mapped to their direction.
    def _get_possible_moves(self, head):
        return {
            "left":  {"x": head["x"] - 1, "y": head["y"]},
            "right": {"x": head["x"] + 1, "y": head["y"]},
            "up":    {"x": head["x"],     "y": head["y"] + 1},
            "down":  {"x": head["x"],     "y": head["y"] - 1},
        }

    # Runs all calculation methods to determine safe and priority moves.
    # Opponent positions are calculated first as they are required by not_enemy_collision.
    def check_moves(self, is_move_safe, **kwargs):

        NEEDED_KEYWORDS = ["head", "game_state", "body", "neck", "my_length"]
        head, game_state, body, neck, my_length = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        self.calculate_opponents_positions(game_state=game_state, my_length=my_length)

        checks = [
            self.calculate_not_backward,
            self.calculate_not_wall_collision,
            self.calculate_not_itself_collision,
            self.calculate_not_enemy_collision,
            self.calculate_food,
        ]

        for check in checks:
            check(is_move_safe, head=head, game_state=game_state, body=body, neck=neck, my_length=my_length)
    
    # Simulates future turns to verify that safe moves remain safe.
    # Reduces the number of simulated turns if no safe moves are found.
    # Falls back to a full reset if an unexpected error occurs.
    def check_safe_moves(self, calls, **kwargs):

        NEEDED_KEYWORDS = ["head", "game_state", "body", "neck", "my_length"]
        head, game_state, body, neck, my_length = self.emergency_system.emergency_system(
            self.keywords.extract_keywords, NEEDED_KEYWORDS, **kwargs
        )

        if calls < 1:
            raise RuntimeError("At least 1 call is required!")

        try:
            while calls > 0:
                copy = deepcopy(self.is_move_safe)

                for move, data in self.is_move_safe.items():
                    if data["is_safe"]:
                        result = self.emergency_system.emergency_system(
                            self.future_safety.call_future_safety, calls,
                            game_state=game_state, body=body, move=move,
                            head=head, my_length=my_length, neck=neck
                        )
                        if self.emergency_system.is_emergency(result):
                            return result
                        if result == False:
                            copy[move]["is_safe"] = False

                # if at least one safe move remains, stop reducing turns
                if any(data["is_safe"] for move, data in copy.items()):
                    break
                else:
                    calls -= 1

            self.is_move_safe = copy
        except Exception as e:
            EmergencyLogger.loger_queue.put(("get_safe_moves", e, self.turn_counter, 40))
            self.reset_is_move_safe()
    
    # Finds the highest priority moves and stores them in priority_moves.
    # If multiple moves share the highest priority, all are kept as candidates.
    def check_priority_moves(self):

        self.reset_priority_moves()

        try:
            priority_counter = 0
            for move, data in self.is_move_safe.items():

                # new highest priority found — replace current candidates
                if data["priority"] > priority_counter:
                    self.priority_moves.clear()
                    self.priority_moves.append(move)
                    priority_counter = data["priority"]

                # tied for highest priority — add as additional candidate
                elif data["priority"] == priority_counter and data["priority"] > 0:
                    self.priority_moves.append(move)
        except Exception as e:
            EmergencyLogger.loger_queue.put(("check_priority_moves", e, self.turn_counter, 40))
            self.priority_moves = []

    # Selects the best available move in order of preference:
    # priority moves → safe moves → emergency moves (fallback).
    # Random selection within each tier to avoid predictable behavior.
    def select_move(self):

        safe_moves = [move for move, data in self.is_move_safe.items() if data["is_safe"]]
        priority_moves = [move for move in safe_moves if move in self.priority_moves]
        EMERGENCY_MOVES = ["left", "right", "up", "down"]

        try:
            if priority_moves:
                next_move = random.choice(priority_moves)
                EmergencyLogger.loger_queue.put(("select_move", "Selected priority move", self.turn_counter, 20))
                return {"move": next_move}

            if safe_moves:
                next_move = random.choice(safe_moves)
                EmergencyLogger.loger_queue.put(("select_move", "Selected safe move", self.turn_counter, 20))
                return {"move": next_move}

            # no safe moves available — fall back to random emergency move
            next_move = random.choice(EMERGENCY_MOVES)
            EmergencyLogger.loger_queue.put(("select_move", "Selected emergency move", self.turn_counter, 40))
            return {"move": next_move}
        except Exception as e:
            EmergencyLogger.loger_queue.put(("select_move", e, self.turn_counter, 40))
            return {"move": random.choice(EMERGENCY_MOVES)}
    
    # Main entry point for move selection.
    # Orchestrates the full pipeline: extract state → check moves → simulate future → select move.
    def choose_move(self, game_state: typing.Dict):

        self.reset_is_move_safe()
        self.future_safety.log_data("choose_move", {"game_state": game_state})

        # extract required game state variables
        try:
            head = game_state["you"]["head"]
            raw_body = game_state["you"]["body"]
            body = self.extract_data.edit_body(raw_body)
            my_length = game_state["you"]["length"]
            self.future_safety.log_data("choose_move", {"head": head, "body": body, "my_length": my_length})
        except Exception:
            raise RuntimeError("game_state is missing or invalid!")

        # get neck position — falls back to emergency move if it fails
        result = self.emergency_system.emergency_system(self.extract_data.get_neck, body=body, game_state=game_state)
        if self.emergency_system.is_emergency(result):
            Move.turn_counter += 1
            return {"move": result["move"]}
        neck = result
        self.future_safety.log_data("choose_move", {"head": head, "neck": neck, "body": body, "my_length": my_length})

        # run all calculation methods to determine safe and priority moves - falls back to emergency move if it fails
        result = self.emergency_system.emergency_system(
            self.check_moves, self.is_move_safe,
            head=head, game_state=game_state, body=body, neck=neck, my_length=my_length
        )
        if self.emergency_system.is_emergency(result):
            Move.turn_counter += 1
            return {"move": result["move"]}
        self.future_safety.log_data("choose_move", {"head": head, "neck": neck, "body": body, "my_length": my_length})

        # simulate future turns to verify safe moves remain safe
        self.check_safe_moves(2, head=head, game_state=game_state, body=body, neck=neck, my_length=my_length)
        self.future_safety.log_data("choose_move", {"head": head, "neck": neck, "body": body, "my_length": my_length})

        self.check_priority_moves()

        Move.turn_counter += 1
        return self.select_move()
    
    # Resets all moves to safe with zero priority before each turn.
    def reset_is_move_safe(self):
        self.is_move_safe = {
            "up":    {"is_safe": True, "priority": 0},
            "down":  {"is_safe": True, "priority": 0},
            "left":  {"is_safe": True, "priority": 0},
            "right": {"is_safe": True, "priority": 0},
        }
        
    # Resets opponent positions before recalculating each turn.
    def reset_opponents_positions(self):
        self.opponents_positions = {}

    # Resets priority moves before recalculating each turn.
    def reset_priority_moves(self):
        self.priority_moves = []

    # Resets the turn counter at the start of a new game.
    @classmethod
    def reset_turn_counter(cls):
        cls.turn_counter = 0
