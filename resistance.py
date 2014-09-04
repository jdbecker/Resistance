from random import shuffle
from player import Player

class Resistance:
    
    """Functions as the game state container for the Resistance game."""
    
    def __init__(self, debug=False):
        """Initializing a new instance of Resistance is essentially starting
        a new game.
        """
        self.debug = debug
        if self.debug: print "New game of Resistance initializing in debug mode..."
        
        # Initialize empty player list
        self.players = []
        self.leader = 0 # Index to players list of current leader
        
        # Initialize mission list
        self.missions = [0,0,0,0,0]
        
        
    def readyCheck(self,players):
        """Return False if any player in players hasn't voted."""
        for player in players:
            if player.vote == 0: return False
        return True
        
        
    def resetVote(self):
        """Reset the vote variable for each player to the neutral 0"""
        for player in self.players:
            player.vote = 0
            
            
    def shufflePlayers(self):
        """Use the shuffle method of random to shuffle the order of the players
        list.
        """
        shuffle(self.players)
        if self.debug:
            print "Players after shuffle:\n"+str([player.name for player in self.players])
        return self.players
        

    def initPlayers(self):
        """loop to populate players list. Called when running in text mode"""
        response = 'y'
        while len(self.players) < 10 and response == 'y':
        # Ensure that the program prompts for new players until the creator is
        # done, or the game is full
            name = raw_input("Name of next player?\n")
            self.players.append( Player(name,debug=self.debug) )
            if 5 <= len(self.players) < 10:
            # If the game isn't full, or under-populated, ask the creator if
            # they want to add another player
                response = ''
                while response not in ('y','n'):
                    response = raw_input("Would you like to add another player?(y/n)\n")
                    if response not in ('y','n'):
                        print "Please respond with just 'y' or 'n'"
        # Print the player list in debug mode
        if self.debug: print [player.name for player in self.players]


    def assignSpies(self):
        """Assume players list is properly populated and shuffle them and
        assign spies.
        """
        # Number of spies should be number of players / 3 rounded up
        numSpies =  -(-len(self.players) // 3)
        
        # create local instance of players for shuffling
        players = self.players
        shuffle(players)
        # grab from the front of the shuffled player list the number of spies
        spies = players[:numSpies]
        
        # Print the names of spies in debug mode
        if self.debug: print "Spies are:\n"+str([spy.name for spy in spies])
        
        
if __name__ == "__main__":
    #li = [0,1,2,3,4]
    #print li[:2]
    game = Resistance(debug=True)
    
    # if this test is being run, assume the program is being tested in text mode
    game.initPlayers()
    
    for player in game.players:
        player.vote = 1
    
    assert game.readyCheck(game.players)
    game.shufflePlayers()
    game.assignSpies()
    game.resetVote()
    assert not game.readyCheck(game.players)