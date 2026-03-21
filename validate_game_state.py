
# Validates that the game state contains all required keys with correct types.
# Returns False if any key is missing, unexpected, or has the wrong type.
def validate_game_state(game_state):

    REQUIRED_KEYS = {
        "game":    dict,
        "ruleset": dict,
        "squad":   dict,
        "turn":    int,
        "board":   dict,
        "you":     dict,
    }

    if not isinstance(game_state, dict):
        return False

    # check all required keys are present
    if not all(key in game_state for key in REQUIRED_KEYS):
        return False

    for key, data in game_state.items():
        if key not in REQUIRED_KEYS:
            return False
        if not isinstance(data, REQUIRED_KEYS[key]):
            return False

    return True