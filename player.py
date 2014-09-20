class Player:
    
    """Container for an individual player for the game Resistance"""
    
    def __init__(self, name, debug=False):
        """A player must be initialized with a name"""
        if debug: print "Initializing new player:",name
        self.name = name
        self.spy = False
        self.vote = 0
        
    def __repr__(self):
        return "Player:%s"%self.name