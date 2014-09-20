class Event(object):
    pass


class Message(Event):
    def __init__(self, message):
        self.message = message


class PlayerJoin(Event):
    def __init__(self, name):
        self.name = name
        
        
class PlayerVote(Event):
    def __init__(self, name, vote):
        self.name = name
        self.vote = vote