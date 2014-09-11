from clientChannel    import ClientChannel
from PodSixNet.Server import Server as psnServer

class Server(psnServer):
    
    """The host runs an instance of the server object. It's job is to
    facilitate communication between the game state object and the client
    objects, of which each player has one.
    """
    
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        self.debug = kwargs.pop('debug', False)
        psnServer.__init__(self, *args, **kwargs)
        if self.debug: print "Server launched in debug mode..."
        
    def Connected(self, channel, addr):
        if self.debug: print addr,"connected"
        
    def update(self):
        self.Pump()
        
###############################################################################
### Tests for Server class
###############################################################################

if __name__ == "__main__":
    server = Server(debug=True)