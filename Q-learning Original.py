import numpy as np
import gym
import gym_foo
import random
import time
from IPython.display import clear_output

env = gym.make('nimWCash-v0')

action_space_size = env.action_space.n
state_space_size = env.observation_space.n

q_table = np.zeros((state_space_size, action_space_size))

num_episodes = 10000
max_steps_per_episode = 100

learning_rate = 0.9
discount_rate = 0.99

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

rewards_all_episodes = []

#generates a table of which player will win based on the starting number of stones
def getWinTable(n, remove):
    flag = False
    winTable = []
    
    #make a table of 0s
    for x in range(n + 1):
        winTable.append(0)

    #trivial cases
    for x in range(min(remove)):
        if x < len(winTable):
            winTable[x] = 2

    for x in remove:
        if x < len(winTable):
            winTable[x] = 1

    #filling out rest of table
    for x in range(n + 1):
        if winTable[x] == 0:
            for y in remove:
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
def getMoveTable(n, remove):

    #initiate variables
    winTable = getWinTable(n, remove)
    moveTable = []
    move = 0
    
    for x in range(n + 1):
        if x < min(remove):
            move = 0
        else:
            for y in remove:
                if x - y >= 0 and winTable[x - y] == 2:
                    move = y
            if move == 0:
                move = min(remove)
        moveTable.append(move)
        move = 0
    return moveTable

def getMove(stones, remove, chance):

        #initialize variable
        possibleMoves = []
        moveTable = getMoveTable(stones, remove)

        #determine the possible moves in current state
        for x in remove:
            if x <= stones:
                possibleMoves.append(x)

        #pick the appropriate move
        if random.uniform(0, 1) < chance:
            move = moveTable[stones]
        else:
            if len(possibleMoves) > 0:
                move = random.choice(possibleMoves)
            else:
                move = 0

        return move

def simulateWinRate(table, startingStones, remove, chance):
    totalWins = 0
    totalGames = 1000
    for n in range(totalGames):
        stones = startingStones
        while(True):
            stonesAfterPlayer2 = -1
            playerOneMove = remove[random.choice(np.where(table[stones,:] == max(table[stones,:]))[0])]
            stonesAfterPlayer1 = stones - playerOneMove
            stones = stonesAfterPlayer1
            if(stonesAfterPlayer1 > 0):
                
                move = getMove(stones, remove, chance)
                    
                stonesAfterPlayer2 = stonesAfterPlayer1 - move
                stones = stonesAfterPlayer2
            if(stonesAfterPlayer1 == 0):
                totalWins += 1
                break
            elif(stonesAfterPlayer2 == 0 or stonesAfterPlayer1 < 0):
                break
    winRate = totalWins/totalGames
    return winRate

allWinRates = []
for episode in range(num_episodes):

    if episode % 10000 == 0:
        winRate = simulateWinRate(q_table, 19, [1, 2, 3], 1)
        allWinRates.append(winRate)
        #print(winRate)
        #print(q_table)
    
    state = env.reset()

    done = False
    rewards_current_episode = 0

    for step in range(max_steps_per_episode):
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > exploration_rate:
            action = np.argmax(q_table[state,:])
        else:
            action = env.action_space.sample()

        new_state, reward, done, info = env.step(action)

        if(state > 0):
            q_table[state, action] = q_table[state, action] * (1 - learning_rate) + learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))

        np.where(q_table[0,:] == max(q_table[0,:]))[0][0]
        state = new_state
        rewards_current_episode += reward

        if done == True:
            break

    exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)

    rewards_all_episodes.append(rewards_current_episode)

rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes), num_episodes/1000)
count = 1000
print("********Average reward per thousand episodes********\n")
for r in rewards_per_thousand_episodes:
    print(count, ": ", str(sum(r/1000)))
    count += 1000
print("\n\n********Q-Table********\n")
print(q_table)
for x in allWinRates:
    print(x)

