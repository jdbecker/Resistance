from PodSixNet.Channel import Channel

class ClientChannel(Channel):

    """An instance of this class is created on the server for each channel
    connected to it. It handles recieving messages on the server.
    """

    def __init__(self, *args, **kwargs):
        self.debug = kwargs.pop('debug', False)
        Channel.__init__(self, *args, **kwargs)
        if self.debug: print "Created channel",self
            
    def __str__(self):
        return str(self.addr)
    
    def Network(self, data):
        if self.debug: print data

###############################################################################
### Tests for ClientChannel class
###############################################################################

if __name__ == "__main__":
    channel = ClientChannel(debug=True)
    print channel