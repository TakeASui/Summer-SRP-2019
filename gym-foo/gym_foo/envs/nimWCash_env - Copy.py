import gym
import random
from gym import error, spaces, utils
from gym.utils import seeding

class NimWCashEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Discrete(216)
        self.startingStones = 5
        self.startingCash1 = 5
        self.startingCash2 = 5
        self.stones = self.startingStones
        self.cash1 = self.startingCash1
        self.cash2 = self.startingCash2
        reward = 0
        done = False

    def getState(self, stones, cash1, cash2):
        state = (cash2) + (self.startingCash2 + 1) * (cash1) + (stones) * (self.startingCash1 + 1) * (self.startingCash2 + 1)
        return state

    def step(self, action):
        done = False
        remove = 0
        if(action == 0):
            remove = 1
        elif(action == 1):
            remove = 2
        else:
            remove = 3
        initialStones = self.stones
        initialCash1 = self.cash1
        initialCash2 = self.cash2
        stonesAfterPlayer1 = self.stones - remove
        cash1 = self.cash1 - remove
        remove = random.randint(1, 3)
        stonesAfterPlayer2 = stonesAfterPlayer1 - remove
        cash2 = self.cash2 - remove

        if cash1 < 0:
            done = True
            reward = -1
            return self.getState(stonesAfterPlayer1, cash1, initialCash2) , reward, done, None
        elif stonesAfterPlayer1 < 0:
            done = True
            reward = -1
            return self.getState(stonesAfterPlayer1, cash1, initialCash2) , reward, done, None
        elif stonesAfterPlayer1 == 0:
            done = True
            reward = 1
            return self.getState(stonesAfterPlayer1, cash1, initialCash2) , reward, done, None
        elif cash2 < 0:
            done = True
            reward = 1
            return self.getState(stonesAfterPlayer2, cash1, cash2) , reward, done, None
        elif stonesAfterPlayer1 > 0:
            reward = 0
        else:
            reward = -1
        self.stones = stonesAfterPlayer2
        self.cash1 = cash1
        self.cash2 = cash2

        return self.getState(stonesAfterPlayer2, cash1, cash2) , reward, done, None
            

    def reset(self):
        self.stones = self.startingStones
        self.cash1 = self.startingCash1
        self.cash2 = self.startingCash2
        return self.getState(self.startingStones, self.startingCash1, self.startingCash2)

    def render(self, mode='human', close=False):
        print("hello world")

    
