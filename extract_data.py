import typing

class ExtractData():

    def __init__(self, keywords):

        self.keywords = keywords
    
    # Appends the current head position to the new body list.
    # Uses None as default to avoid mutable default argument pitfall.
    def get_body(self, new_body: typing.List[dict] = None, **kwargs):

        NEEDED_KEYWORDS = ["head"]
        head, = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        if new_body is None:
            new_body = []

        new_body.append(head)
        return new_body
    
    # Simulates the body after a move — shifts each body part forward
    # and drops the tail, keeping the length equal.
    def call_get_body(self, **kwargs):

        NEEDED_KEYWORDS = ["head", "body"]
        head, body = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        new_body = None
        calls = 0
        required_calls = len(body)

        for body_part in body:

            if calls == required_calls:
                return new_body

            # append current head to new body
            new_body = self.get_body(new_body, head=head)

            # each body part becomes the next head in the shift
            head = body_part
            calls += 1

        return new_body
    
    # Returns the neck position (second body part).
    # Falls back to body[0] on turn 0 when the body has only one segment.
    def get_neck(self, **kwargs):

        NEEDED_KEYWORDS = ["body"]
        body, = self.keywords.extract_keywords(NEEDED_KEYWORDS, **kwargs)

        try:
            return body[1]
        except IndexError:
            # turn 0 edge case — body has only one segment
            try:
                return body[0]
            except IndexError:
                raise IndexError("Body is empty")
            
    # Returns the length of the snake's body.
    def get_length(self, body):
        return len(body)
    
    # Removes duplicate body parts — on turn 0 the Battlesnake engine
    # initializes three identical segments at the same position.
    def edit_body(self, body):
        new_body = []
        for seg in body:
            if seg not in new_body:
                new_body.append(seg)
        return new_body
    
    