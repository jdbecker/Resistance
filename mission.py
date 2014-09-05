from player import Player

class Mission:
    
    """An instance of Mission is needed for each mission of Resistance game.
    Should include a result variable which is 0 if the mission isn't complete
    yet, -1 if spies won, and +1 if resistance won. Should also include methods
    for choosing a team, voting for a team, and voting for pass/fail of the
    mission itself.
    """
    
    def __init__(self, missionNumber, players, debug=False):
        """All missions will be created from the beginning of the game, so at
        that point all that will be known about each mission is that the result
        is 0 (for undetermined), the missionNumber, and the list of players
        in the game (for determining the number of team members required).
        """
        self.debug = debug
        if self.debug: print "Creating mission in debug mode..."
        teamMemberTable = [
  # Players: 5  6  7  8  9  10  # Mission
            [2, 2, 2, 3, 3, 3], # 1
            [3, 3, 3, 4, 4, 4], # 2
            [2, 4, 3, 4, 4, 4], # 3
            [3, 3, 4, 5, 5, 5], # 4
            [3, 4, 4, 5, 5, 5]] # 5
          
        self.players = players
        if self.debug: print "number of players:", len(self.players)
        self.missionNumber = missionNumber
        self.missionIndex = missionNumber-1
        if self.debug: print "mission number:", self.missionNumber
        self.result = 0
        self.teamSize = teamMemberTable[self.missionIndex][len(players)-5]
        if self.debug: print "required team size:", self.teamSize
        self.team = []
        self.voteAttempts = 0 # If the players fail to assemble a team 5 times
                              # in a row, the resistance loses the game
        
        
    def failToCreateTeam(self):
        """Call each time a team fails to be voted for, to increment the
        voteAttempts and check if resistance loses the game.
        """
        if len(self.team) == self.teamSize:
            if self.debug: print "Team of size",len(self.team),"created successfully!"
            return False
        if self.debug: print len(self.team),"doesn't meet required team size",self.teamSize
        self.voteAttempts += 1
        if self.voteAttempts >= 5:
            self.result = -5 # -5 signifies losing not only the mission, but the entire game
        return True
        
        
    def attempt(self):
        """Assume that a team has been arranged, and all team members have
        voted on whether to pass or fail the mission. Modify self.result, if
        any players chose to fail the mission make it -1, otherwise +1.
        """
        if len(self.team) == self.teamSize:
            if self.debug: print "Can't attempt mission with only "+ str(len(self.team))+" team members."
            return False
        assert self.result == 0, "Can't re-attempt mission."
        votes = []
        for player in self.team:
            assert player.vote != 0, "Every team member must vote to attempt."
            if self.debug: print player.name,"votes",player.vote
            votes.append(player.vote)
        votes.sort() # Sort the votes to protect the identity of the voters
        if self.debug: print "votes:",votes
        if votes[0] == -1:
                self.result = -1
                return votes
        self.result = 1
        return votes
        
        
        
if __name__ == "__main__":
    numPlayers = 5
    misNum = 5
    mission = Mission(misNum, [Player(str(name+1)) for name in range(numPlayers)], debug=True)
    mission.team = mission.players[:mission.teamSize]
    for player in mission.team:
        player.vote = 1
    mission.team[2].vote = -1
    mission.attempt()
    print mission.result