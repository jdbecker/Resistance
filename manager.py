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
    from events import PlayerJoin
    
    game = Resistance(debug=True)
    manager = Manager()
    
    manager.register(game)
    manager.post(PlayerJoin("Karl"))