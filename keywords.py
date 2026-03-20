
import typing

class Keywords():

    def __init__(self):

        self.ALLOWED_KEYWORDS =  ["head", "game_state", "body", "neck", "snake", "calls", "move", "new_head", "safe_moves", "memory_moves", "my_length"]
        self.DICTIONARY_KEYS = ["head", "game_state", "neck", "new_head", "safe_moves", "snake"]
        self.LIST_KEYS = ["body", "memory_moves"]
        self.STRING_KEYS = ["move"]
        self.INTEGER_KEYS = ["calls", "my_length"]
        self.FLOAT_KEYS = []
    
    # Filters kwargs to only include allowed keywords.
    # Silently ignores any kwargs that are not in the allowed list.
    def get_allowed_keywords(self, **kwargs):

        ALLOWED_KEYWORDS = [
            "head", "game_state", "body", "neck", "snake",
            "calls", "move", "new_head", "safe_moves", "memory_moves", "my_length"
        ]

        return {key: kwargs[key] for key in ALLOWED_KEYWORDS if key in kwargs}
    
    # Validates that each keyword matches its expected type.
    # Raises TypeError if a keyword has the wrong type, RuntimeError if it is unlisted.
    def check_datatype(self, keywords: typing.Dict):

        TYPE_MAP = {
            "head":         dict,
            "game_state":   dict,
            "neck":         dict,
            "new_head":     dict,
            "safe_moves":   dict,
            "snake":        dict,
            "body":         list,
            "memory_moves": list,
            "move":         str,
            "calls":        int,
            "my_length":    int,
        }

        for key, value in keywords.items():
            if key not in TYPE_MAP:
                raise RuntimeError(f"{key} is not a listed keyword")

            expected_type = TYPE_MAP[key]
            if not isinstance(value, expected_type):
                raise TypeError(f"{key} requires type {expected_type.__name__}")
    
    # Extracts and validates required keywords from kwargs.
    # Raises KeyError if a required keyword is missing.
    def extract_keywords(self, needed_keywords: typing.List[str], **kwargs):

        keywords = self.get_allowed_keywords(**kwargs)
        self.check_datatype(keywords)

        found_keywords = []
        for keyword in needed_keywords:
            if keyword not in keywords:
                raise KeyError(f"{keyword} is required!")
            found_keywords.append(keywords[keyword])

        return found_keywords