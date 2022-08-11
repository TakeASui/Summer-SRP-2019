import gym
import random
from gym import error, spaces, utils
from gym.utils import seeding

class NimWCashEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.stones = 15
        self.cash1 = 15
        self.cash2 = 15
        self.rules = [1, 2, 3]
        self.action_space = spaces.Discrete(len(self.rules))
        self.observation_space = spaces.Discrete((self.stones + 1) * (self.cash1 + 1) * (self.cash2 + 1))
        self.startingStones = self.stones
        self.startingCash1 = self.cash1
        self.startingCash2 = self.cash2
        self.chance = 0
        self.moveTable = NimWCashEnv.getMoveTable(self)
        reward = 0
        done = False

    def getWinTable(self):
        flag = False
        winTable = []
        greaterCashAmount = max(self.startingCash1 + 1, self.startingCash2 + 1)

        #make a table of 0s
        for x in range(self.startingStones + 1):
            winTable.append([])
            for y in range(greaterCashAmount):
                winTable[x].append([])
                for z in range(greaterCashAmount):
                    winTable[x][y].append(0)

        #trivial cases
        for x in range(self.startingStones + 1):
            for y in range(greaterCashAmount):
                for z in range(greaterCashAmount):
                    if x < min(self.rules): #too little stones left on the board
                        winTable[x][y][z] = 2
                    elif y < min(self.rules): #player one out of cash
                        winTable[x][y][z] = 2
                    elif z < min(self.rules): #player two out of cash
                        winTable[x][y][z] = 1
                        
        for i in range(self.startingStones + 1):
            for cash1 in range(greaterCashAmount):
                for cash2 in range(greaterCashAmount):
                    if winTable[i][cash1][cash2] == 0:
                        for x in self.rules:
                            if i - x >= 0 and cash1 - x >= 0 and winTable[i - x][cash2][cash1 - x] == 2:
                                flag = True
                        if flag:    
                            winTable[i][cash1][cash2] = 1
                        else:
                            winTable[i][cash1][cash2] = 2
                    flag = False
       
        return winTable

    def getMoveTable(self):
        winTable = NimWCashEnv.getWinTable(self)
        moveTable = []
        move = 0
        greaterCashAmount = max(self.startingCash1 + 1, self.startingCash2 + 1)

        #make a table of 0s
        for x in range(self.startingStones + 1):
            moveTable.append([])
            for y in range(greaterCashAmount):
                moveTable[x].append([])
                for z in range(greaterCashAmount):
                    moveTable[x][y].append(0)


        for i in range(self.startingStones + 1):
            for cash1 in range(greaterCashAmount):
                for cash2 in range(greaterCashAmount):
                    if i < min(self.rules): #too little stones left on the board
                        moveTable[i][cash1][cash2] = 0
                        
                    elif cash1 < min(self.rules): #player one out of cash
                        moveTable[i][cash1][cash2] = 0

                    elif cash2 < min(self.rules): #don't make a move if player two is out of cash
                        moveTable[i][cash1][cash2] = 0
                        
                    else:
                        for x in self.rules:
                            if i - x >= 0 and cash1 - x >= 0 and winTable[i - x][cash2][cash1 - x] == 2:
                                move = x

                        #if there are no winning moves, remove the least amount of stones
                        if move == 0:
                            move = min(self.rules)
                    
                        moveTable[i][cash1][cash2] = move
                        move = 0
       
        return moveTable

    def getMove(self, stones, cash1, cash2):

        #initialize variable
        possibleMoves = []

        #determine the possible moves in current state
        for x in self.rules:
            if x <= stones and x <= cash1:
                possibleMoves.append(x)

        #pick the appropriate move
        if random.uniform(0, 1) < self.chance:
            move = self.moveTable[stones][cash1][cash2]
        else:
            if len(possibleMoves) > 0:
                move = random.choice(possibleMoves)
            else:
                move = 0

        return move

    def getState(self, stones, cash1, cash2):
        state = (cash2) + (self.startingCash2 + 1) * (cash1) + (stones) * (self.startingCash1 + 1) * (self.startingCash2 + 1)
        return state

    def step(self, action):
        done = False
        playerOneMove = self.rules[action]
        initialStones = self.stones
        initialCash1 = self.cash1
        initialCash2 = self.cash2
        stonesAfterPlayer1 = self.stones - playerOneMove
        cash1 = initialCash1 - playerOneMove

        if(stonesAfterPlayer1 > 0 and initialCash2 > 0 and cash1 > 0):
            playerTwoMove = NimWCashEnv.getMove(self, stonesAfterPlayer1, initialCash2, cash1)
        else:
            playerTwoMove = 0
            
        stonesAfterPlayer2 = stonesAfterPlayer1 - playerTwoMove
        cash2 = initialCash2 - playerTwoMove  

        if cash1 < 0:
            done = True
            reward = -2
        elif stonesAfterPlayer1 < 0:
            done = True
            reward = -2
        elif stonesAfterPlayer1 == 0:
            done = True
            reward = 1
        elif playerTwoMove == 0:
            done = True
            reward = -1
        else:
            reward = 0

        if(stonesAfterPlayer2 < 0):
            self.stones = 0
        else:
            self.stones = stonesAfterPlayer2

        if(cash1 < 0):
            self.cash1 = 0
        else:
            self.cash1 = cash1

        if(cash2 < 0):
            self.cash2 = 0
        else:
            self.cash2 = cash2

        return self.getState(self.stones, self.cash1, self.cash2) , reward, done, None
            

    def reset(self):
        self.stones = self.startingStones
        self.cash1 = self.startingCash1
        self.cash2 = self.startingCash2
        return self.getState(self.startingStones, self.startingCash1, self.startingCash2)

    def render(self, mode='human', close=False):
        print("hello world")

    
