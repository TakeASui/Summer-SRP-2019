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
def getWinTable(n, d, e, remove):
    flag = False
    winTable = []

    #make a table of 0s
    for x in range(n + 1):
        winTable.append([])
        for y in range(max(d + 1, e + 1)):
            winTable[x].append([])
            for z in range(max(d + 1, e + 1)):
                winTable[x][y].append(0)

    #trivial cases
    for x in range(n + 1):
        for y in range(max(d + 1, e + 1)):
            for z in range(max(d + 1, e + 1)):
                if x < min(remove): #too little stones left on the board
                    winTable[x][y][z] = 2
                elif y < min(remove): #player one out of cash
                    winTable[x][y][z] = 2
                elif z < min(remove): #player two out of cash
                    winTable[x][y][z] = 1
                    
    for i in range(n + 1):
        for cash1 in range(max(d + 1, e + 1)):
            for cash2 in range(max(d + 1, e + 1)):
                if winTable[i][cash1][cash2] == 0:
                    for x in remove:
                        if i - x >= 0 and cash1 - x >= 0 and winTable[i - x][cash2][cash1 - x] == 2:
                            flag = True
                    if flag:    
                        winTable[i][cash1][cash2] = 1
                    else:
                        winTable[i][cash1][cash2] = 2
                flag = False
   
    return winTable

#generates a list of the best move in nim based on how many stones are on the board
def getMoveTable(n, d, e, remove):
    winTable = getWinTable(n, d, e, remove)
    moveTable = []
    move = 0

    #make a table of 0s
    for x in range(n + 1):
        moveTable.append([])
        for y in range(max(d + 1, e + 1)):
            moveTable[x].append([])
            for z in range(max(d + 1, e + 1)):
                moveTable[x][y].append(0)


    for i in range(n + 1):
        for cash1 in range(max(d + 1, e + 1)):
            for cash2 in range(max(d + 1, e + 1)):
                if i < min(remove): #too little stones left on the board
                    moveTable[i][cash1][cash2] = 0
                    
                elif cash1 < min(remove): #player one out of cash
                    moveTable[i][cash1][cash2] = 0
                    
                else:
                    for x in remove:
                        if i - x >= 0 and cash1 - x >= 0 and winTable[i - x][cash2][cash1 - x] == 2:
                            move = x

                    #if there are no winning moves, remove the least amount of stones
                    if move == 0:
                        move = min(remove)
                
                    moveTable[i][cash1][cash2] = move
                    move = 0
   
    return moveTable

def getMove(stones, cash1, cash2, remove, chance):

        #initialize variable
        possibleMoves = []
        moveTable = getMoveTable(stones, cash1, cash2, remove)

        #determine the possible moves in current state
        for x in remove:
            if x <= stones:
                possibleMoves.append(x)

        #pick the appropriate move
        if random.uniform(0, 1) < chance:
            move = moveTable[stones][cash1][cash2]
        else:
            if len(possibleMoves) > 0:
                move = random.choice(possibleMoves)
            else:
                move = 0

        return move

def getState(startingCash1, startingCash2, stones, cash1, cash2):
        state = (cash2) + (startingCash2 + 1) * (cash1) + (stones) * (startingCash1 + 1) * (startingCash2 + 1)
        return state

def simulateWinRate(table, startingStones, startingCash1, startingCash2, remove, chance):
    totalWins = 0
    totalGames = 1
    for n in range(totalGames):
        stones = startingStones
        cash1 = startingCash1
        cash2 = startingCash2
        while(True):
            stonesAfterPlayer2 = -1
            state = getState(startingCash1, startingCash2, stones, cash1, cash2)
            playerOneMove = remove[random.choice(np.where(table[state,:] == max(table[state,:]))[0])]
            stonesAfterPlayer1 = stones - playerOneMove
            cash1 -= playerOneMove
            stones = stonesAfterPlayer1
            print("Stones After Player One:", stonesAfterPlayer1)
            print("Player One Cash:", cash1)
            if(stonesAfterPlayer1 > 0 and cash1 >= 0):
                
                move = getMove(stones, cash2, cash1, remove, chance)
                    
                stonesAfterPlayer2 = stonesAfterPlayer1 - move
                cash2 -= move
                stones = stonesAfterPlayer2
                print("Stones After Player Two:", stonesAfterPlayer2)
                print("Player Two Cash:", cash2)
            if(cash1 < 0):
                break
            elif(stonesAfterPlayer1 == 0):
                totalWins += 1
                break
            elif(stonesAfterPlayer2 == 0 or stonesAfterPlayer1 < 0):
                break
            elif(move == 0):
                totalWins += 1
                break
    winRate = totalWins/totalGames
    return winRate

allWinRates = []
for episode in range(num_episodes):

    if episode % 1000 == 0:
        print(episode)
        winRate = simulateWinRate(q_table, 15, 15, 15, [1, 2, 3], 1)
        allWinRates.append(winRate)
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

