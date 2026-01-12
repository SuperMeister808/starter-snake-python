
def validate_game_state(game_state):

        important_keys = ["game", "ruleset", "squad", "turn", "board", "you"]

        for key , data in game_state.items():

            if key != important_keys:

                return False
            
            if not isinstance(data, dict):

                return False
            
        return True