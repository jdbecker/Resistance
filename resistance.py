from listener import Listener
from random  import shuffle
from player  import Player
from mission import Mission
import events

class Resistance(Listener):
    
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
        self.proposedTeam = []
        
        # Initialize mission list
        self.missions = []

        
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
            print "First leader will be",self.players[self.leader].name
        return self.players
        
        
    def nameTaken(self, name):
        """Check that a player does not already exist with the prospective name"""
        for player in self.players:
            if player.name == name: return True
        return False
        
        
    def checkVote(self):
        """Check if all the votes have been gathered for the appropriate stage
        of the game, and kick-off the appropriate methods if so.
        """
        if self.nextMission(): # Voting is for some part of the next mission
            mission = self.nextMission()
            if mission.team: # voting is to decide if the mission succeeds
                if not self.readyCheck(mission.team): return False
                else: return self.attemptNextMission()
                
            else: # voting is to decide if the proposed mission team is deployed
                if not self.readyCheck(self.players): return False
                else: return self.createTeam()
                
        else: # Missions have not been created yet, still in setup
            if not self.readyCheck(self.players): return False
            else: return self.initPlayers()
        

    def initPlayers(self):
        """Call when players are done joining. Check that player limits are
        met and call other setup functions, such as shuffling players,
        assigning spies, and shuffling missions."""
        if self.debug: print "Locking in and initializing %d player game"%len(self.players)
        assert 5 <= len(self.players) <= 10, "Must have between 5 and 10 players. You have "+str(len(self.players))
        self.initMissions()
        self.shufflePlayers()
        self.assignSpies()
            
            
    def initMissions(self):
        """Assume players list is populated and won't be changing anymore.
        Populate the mission list with new Mission objects.
        """
        assert 5 <= len(self.players) <= 10
        for i in range(5):
            misNum = i+1
            self.missions.append(Mission(misNum, self.players, debug=self.debug))
            
            
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
        for player in spies:
            player.spy = True
        
        
    def nextMission(self):
        """return the lowest index mission in missions that still has a result
        of 0.
        """
        if not self.missions: return None
        for mission in self.missions:
            if mission.result == 0:
                if self.debug: print "next Mission returned:",mission.missionNumber
                return mission
        assert False, "No nextMission found!"
        
        
    def nextLeader(self):
        """Increments the self.leader to represent the index of the next leader"""
        leader = self.leader + 1
        if leader >= len(self.players):
            self.leader = 0
        else:
            self.leader = leader
        if self.debug: print self.players[self.leader].name, "is the new leader."
        
        
    def createTeam(self):
        """Evaluate if the vote passed to create the team. If it did, insert
        the proposed team into the current mission. If it did not, call the
        mission's failToCreateTeam method."""
        assert len(self.proposedTeam) == self.nextMission().teamSize, "Proposed team not big enough:"+str([player.name for player in self.proposedTeam])
        votes = []
        for player in self.players:
            assert player.vote != 0, "Each player must vote on the proposed team."
            votes.append(player.vote)
        total = 0
        for vote in votes:
            total += vote
        if total > 0:
            self.nextMission().team = self.proposedTeam
        self.nextMission().failToCreateTeam()
        self.resetVote()
        
        
    def attemptNextMission(self):
        """Attempt the current mission. Requires that the team has already
        been set and that each team member has already voted. Will modify the
        mission result appropriately and clear the vote.
        """
        votes = self.nextMission().attempt()
        if self.debug: print "Votes tally:", votes
        self.resetVote()
        
        
    def spiesWin(self):
        """Return True if the spies have won the game."""
        standings    = 0
        missionsLeft = 0        
        for mission in self.missions:
            if mission.result == 0:
                missionsLeft += 1
            standings += mission.result
        win = standings + missionsLeft < 0
        if self.debug: print "standings,missionsLeft:",standings,missionsLeft
        if self.debug: print "Spies win?", win
        return win
        
        
    def resistanceWin(self):
        """Return True if the resistance have won the game."""
        standings    = 0
        missionsLeft = 0
        for mission in self.missions:
            if mission.result == 0:
                missionsLeft += 1
            standings += mission.result
        win = standings - missionsLeft > 0
        if self.debug: print "standings,missionsLeft:",standings,missionsLeft
        if self.debug: print "Resistance win?", win
        return win
        
        
    # Event handling:
    def getEvent(self, event):
        """If registered as a listener with an manager, this method will be
        called whenever a new event is posted.
        """
        if self.debug: print "Received event:",type(event)
            
        # Player Join
        if type(event) == events.PlayerJoin:
            if len(self.players) < 10:
                if self.nameTaken(event.name):
                    return self.manager.post(events.Message("The name '%s' is already taken. Please choose another."%event.name))
                self.manager.post(events.Message("Player %s joined"%event.name))
                self.players.append(Player(event.name))
                return
            else:
                self.manager.post(events.Message("Player %s tried to join, but there are already 10 players!"%event.name))
                return
                
        # Player Vote
        if type(event) == events.PlayerVote:
            for player in self.players:
                if player.name == event.name:
                    player.vote = event.vote
            return self.checkVote()
                
        # Receive Message
        if type(event) == events.Message:
            print event.message
            return
        
        
if __name__ == "__main__":
    #li = [0,1,2,3,4]
    #print li[:2]
    game = Resistance(debug=True)
    
    # if this test is being run, assume the program is being tested in text mode
    game.players = [Player("Player"+str(name+1)) for name in range(5)]
    
    for player in game.players:
        player.vote = 1
    
    assert game.readyCheck(game.players)
    game.shufflePlayers()
    game.assignSpies()
    game.resetVote()
    assert not game.readyCheck(game.players)
    
    game.initMissions()
    game.spiesWin()
    game.resistanceWin()
    
    game.nextMission().result = 1
    game.nextMission().result = 1
        
    game.spiesWin()
    game.resistanceWin()
    
    for i in range(5):
        game.nextMission().failToCreateTeam()
    print "failed mission result:",game.missions[2].result
    
    game.spiesWin()
    game.resistanceWin()
    
    assert game.nextMission().result == 0
    del game
    
    ###########
    # Newgame #
    ###########
    print "\n\n"
    game = Resistance(debug=True)
    
    # Add 7 players
    game.players = [Player("Player"+str(name+1)) for name in range(7)]
    
    # Lock-in and initialize the 7 player game
    game.initPlayers()
    
    # Begin Game Loop
    while not game.spiesWin() and not game.resistanceWin():
        
        #leader proposes a team
        proposedTeam = game.players
        shuffle(proposedTeam)
        game.proposedTeam = proposedTeam[:game.nextMission().teamSize]
        
        # players vote on the team
        for player in game.players:
            player.vote = 1
        game.createTeam()

        if not game.nextMission().failToCreateTeam():
            # players on the team vote for the mission
            for player in game.nextMission().team:
                if player.spy:
                    player.vote = -1
                else:
                    player.vote =  1
            game.attemptNextMission()
            
        game.nextLeader()