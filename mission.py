from player import Player

class Mission:
    
    """An instance of Mission is needed for each mission of Resistance game.
    Should include a result variable which is 0 if the mission isn't complete
    yet, -1 if spies won, and +1 if resistance won. Should also include methods
    for choosing a team, voting for a team, and voting for pass/fail of the
    mission itself.
    """
    
    def __init__(self, missionNumber, players):
        """All missions will be created from the beginning of the game, so at
        that point all that will be known about each mission is that the result
        is 0 (for undetermined), the missionNumber, and the list of players
        in the game (for determining the number of team members required).
        """
        teamMemberTable = [
  # Players: 5  6  7  8  9  10  # Mission
            [2, 2, 2, 3, 3, 3], # 1
            [3, 3, 3, 4, 4, 4], # 2
            [2, 4, 3, 4, 4, 4], # 3
            [3, 3, 4, 5, 5, 5], # 4
            [3, 4, 4, 5, 5, 5]] # 5
          
        self.players = players
        self.missionNumber = missionNumber
        self.result = 0
        self.teamSize = teamMemberTable[missionNumber][len(players)-5]
        self.team = []
        
        
if __name__ == "__main__":
    numPlayers = 10
    misNum = 4
    mission = Mission((misNum-1),[Player(str(name+1)) for name in range(numPlayers)])
    print mission.missionNumber,len(mission.players),mission.teamSize