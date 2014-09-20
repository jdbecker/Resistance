from weakref import WeakKeyDictionary

class Manager:
    
    """Keeps a list of registered 'listeners' and sends each of them events
    that they might be interested in.
    """
    
    def __init__(self):
        # Uses WeakKey because if listener is deleted elsewhere, this does not
        # need to continue referencing it.
        self.listeners = WeakKeyDictionary()
        
    def register(self, listener):
        """Adds listener to the list of registered listeners."""
        listener.manager = self
        self.listeners[listener] = 1
        
    def unregister(self, listener):
        """Remove a listener from the list of registered listeners."""
        self.listeners.pop(listener, None)
        
    def post(self, event):
        """Forward the given event to all listeners"""
        for listener in self.listeners:
            listener.getEvent(event)
            
            
if __name__ == "__main__":
    from resistance import Resistance
    from events import PlayerJoin, PlayerVote
    
    game = Resistance(debug=True)
    manager = Manager()
    
    manager.register(game)
    manager.post(PlayerJoin("Karl"))
    manager.post(PlayerJoin("Tim"))
    manager.post(PlayerJoin("Tim"))    
    manager.post(PlayerJoin("Sam"))
    manager.post(PlayerJoin("Kim"))
    manager.post(PlayerJoin("Alex"))
    manager.post(PlayerJoin("Sarah"))
    manager.post(PlayerJoin("George"))
    manager.post(PlayerJoin("Fred"))
    manager.post(PlayerJoin("Betty"))
    manager.post(PlayerJoin("Lester"))
    manager.post(PlayerJoin("Bob"))
    
    manager.post(PlayerVote("Karl",1))
    manager.post(PlayerVote("Tim",1))
    manager.post(PlayerVote("Tim",1))    
    manager.post(PlayerVote("Sam",1))
    manager.post(PlayerVote("Kim",1))
    manager.post(PlayerVote("Alex",1))
    manager.post(PlayerVote("Sarah",1))
    manager.post(PlayerVote("George",1))
    manager.post(PlayerVote("Fred",1))
    manager.post(PlayerVote("Betty",1))
    manager.post(PlayerVote("Lester",1))
