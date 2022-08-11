import gym
import random
from gym import error, spaces, utils
from gym.utils import seeding

class NimEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.stones = 25
        self.rules = [1, 2, 3]
        self.startingStones = self.stones
        self.action_space = spaces.Discrete(len(self.rules))
        self.observation_space = spaces.Discrete(self.stones + 1)
        self.chance = 0
        reward = 0
        done = False

    #generates a table of which player will win based on the starting number of stones
    def getWinTable(self):
        flag = False
        winTable = []
        
        #make a table of 0s
        for x in range(self.startingStones + 1):
            winTable.append(0)

        #trivial cases
        for x in range(min(self.rules)):
            if x < len(winTable):
                winTable[x] = 2

        for x in self.rules:
            if x < len(winTable):
                winTable[x] = 1

        #filling out rest of table
        for x in range(self.startingStones + 1):
            if winTable[x] == 0:
                for y in self.rules:
                    if winTable[x - y] == 2:
                        flag = True
                if flag:
                    winTable[x] = 1
                else:
                    winTable[x] = 2
            flag = False

        #return win table
        return winTable

    #generates a list of the best move in nim based on how many stones are on the board
    def getMoveTable(self):

        #initialize variables
        winTable = NimEnv.getWinTable(self)
        moveTable = []
        move = 0
        
        for x in range(self.startingStones + 1):
            if x < min(self.rules):
                move = 0
            else:
                for y in self.rules:
                    if x - y >= 0 and winTable[x - y] == 2:
                        move = y
                if move == 0:
                    move = min(self.rules)
            moveTable.append(move)
            move = 0
        return moveTable
    
    def getMove(self, stones):

        #initialize variable
        possibleMoves = []
        moveTable = NimEnv.getMoveTable(self)

        #determine the possible moves in current state
        for x in self.rules:
            if x <= stones:
                possibleMoves.append(x)

        #pick the appropriate move
        if random.uniform(0, 1) < self.chance:
            move = moveTable[stones]
        else:
            if len(possibleMoves) > 0:
                move = random.choice(possibleMoves)
            else:
                move = 0

        return move
            
    def step(self, action):
        done = False
        remove = self.rules[action]
        initialStones = self.stones
        stonesAfterPlayer1 = self.stones - remove
        stonesAfterPlayer2 = stonesAfterPlayer1 - NimEnv.getMove(self, stonesAfterPlayer1)
        if stonesAfterPlayer1 < 0:
            done = True
            reward = -2
        elif stonesAfterPlayer1 == 0:
            done = True
            reward = 1
        elif stonesAfterPlayer1 > 0:
            reward = 0
        else:
            reward = -1
        if(stonesAfterPlayer2 < 0):
            self.stones = 0
        else:
            self.stones = stonesAfterPlayer2

        return self.stones, reward, done, None
            

    def reset(self):
        self.stones = self.startingStones
        return self.stones

    def render(self, mode='human', close=False):
        print("hello world")

    
