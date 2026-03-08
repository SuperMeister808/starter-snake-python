
import typing

class Keywords():

    def __init__(self):

        self.ALLOWED_KEYWORDS =  ["head", "game_state", "body", "neck", "snake", "calls", "move", "new_head", "safe_moves", "memory_moves", "my_length"]
        self.DICTIONARY_KEYS = ["head", "game_state", "neck", "new_head", "safe_moves", "snake"]
        self.LIST_KEYS = ["body", "memory_moves"]
        self.STRING_KEYS = ["move"]
        self.INTEGER_KEYS = ["calls", "my_length"]
        self.FLOAT_KEYS = []
    
    def get_allowed_keywords(self, **kwargs):

        ALLOWED_KEYWORDS = ["head", "game_state", "body", "neck", "snake", "calls", "move", "new_head", "safe_moves", "memory_moves", "my_length"]
        keywords = {}

        for allowed_keyword in self.ALLOWED_KEYWORDS:
            try:
                keyword = kwargs[allowed_keyword]
                keywords[allowed_keyword] = keyword
            except KeyError as e:
                continue
        
        return keywords
    
    def check_datatype(self, keywords: typing.Dict):

        DICTIONARY_KEYS = ["head", "game_state", "neck", "new_head", "safe_moves", "snake"]
        LIST_KEYS = ["body", "memory_moves"]
        STRING_KEYS = ["move"]
        INTEGER_KEYS = ["calls", "my_length"]
        FLOAT_KEYS = []

        for key , keyword in keywords.items():
            
            listed = False
            
            if key in self.DICTIONARY_KEYS:
                listed = True
                if not isinstance(keyword, dict):
                    raise TypeError(f"{key} als Dictionary erforderlich!")
                
            if key in self.LIST_KEYS:
                listed = True
                if not isinstance(keyword, list):
                    raise TypeError(f"{key} als Liste erforderlich!")
                
            if key in self.STRING_KEYS:
                listed = True
                if not isinstance(keyword, str):
                    raise TypeError(f"{key} als String erforderlich!")
                
            if key in self.INTEGER_KEYS:
                listed = True
                if not isinstance(keyword, int):
                    raise TypeError(f"{key} als Integer erforderlich!")
                
            if key in self.FLOAT_KEYS:
                listed = True
                if not isinstance(keyword, float):
                    raise TypeError(f"{key} als Float erforderlich!")
                
            if listed == False:
                raise RuntimeError(f"{key} nicht gelisted")
    
    def extract_keywords(self, needed_keywords: typing.List[str], **kwargs):


        keywords = self.get_allowed_keywords(**kwargs)

        self.check_datatype(keywords)

        found_keywords = []
        for keyword in needed_keywords:
            if keyword not in keywords:
                raise KeyError(f"{keyword} erforderlich!")
            found_keywords.append(keywords[keyword])

        return found_keywords