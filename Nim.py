#generates a table of which player will win based on the starting number of stones
def nim(n, remove):
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
def nimMove(n, remove):

    #initiate variables
    winTable = nim(n, remove)
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

#Plays a game of nim with the computer
def playNim(n, remove):
    moveTable = nimMove(n, remove)
    stones = n
    playerOneMove = 0
    playerTwoMove = 0
    
    while(True):
        #determine the computer's move
        playerOneMove = moveTable[stones]

        #no possible moves
        if playerOneMove == 0:
            print("Player one has no possible moves, you have won")
            break

        #adjust number of stones
        stones -= playerOneMove

        #output
        print("Player one removes", playerOneMove, "stones, there are", stones, "stones left")

        #determine whether computer has won
        if stones < min(remove):
            print("The computer has won")
            break
        
        #input protection
        while(not playerTwoMove in remove):
            playerTwoMove = int(input("Enter number of stones to remove: "))

        #adjust number of stones
        stones -= playerTwoMove
        
        #reset the move
        playerTwoMove = 0

        #output
        print("There are", stones, "stones left")

        #determine whether player two has won
        if stones < min(remove):
            print("You have won")
            break
