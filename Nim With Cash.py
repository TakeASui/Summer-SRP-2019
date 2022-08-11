def nimWithCash(n, d, e, remove):
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

def nimWithCashMove(n, d, e, remove):
    winTable = nimWithCash(n, d, e, remove)
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

#When computer goes second
def playNimWithCash1(n, d, e, remove):

    #initiate variables
    moveTable = nimWithCashMove(n, d, e, remove)
    stones = n
    playerOneCash = d
    playerTwoCash = e
    playerOneMove = 0
    playerTwoMove = 0

    while(True):

        #determine whether computer has won
        if stones < min(remove):
            print("You can't remove any more stones. The computer has won")
            break
        elif playerOneCash < min(remove):
            print("You have run out of money. The computer has won")
            break
        
        #input protection
        playerOneMove = int(input("Enter number of stones to remove: "))
        while(not playerOneMove in remove or not playerOneMove <= playerOneCash or playerOneMove > stones):
            if(not playerOneMove in remove):
                playerOneMove = int(input("That is not a possible number of stone to be removed, enter another value: "))
            elif(not playerOneMove <= playerOneCash):
                playerOneMove = int(input("You do not have enough cash to play that move, enter another value: "))
            elif(playerOneMove > stones):
                playerOneMove = int(input("There are not enough stones left for you to play that move, enter another value: "))

        #adjust variables accordingly
        stones -= playerOneMove
        playerOneCash -= playerOneMove
        
        #reset the move
        playerOneMove = 0

        #output
        print("Stones left:", stones)
        print("Player one cash:", playerOneCash)
        print("player two cash:", playerTwoCash)

        #determine whether player two has won
        if stones < min(remove):
            print("You have won")
            break
        elif playerTwoCash < min(remove):
            print("You have won")
            break

        #determine the computer's move
        playerTwoMove = moveTable[stones][playerTwoCash][playerOneCash]

        #no possible moves
        if playerTwoMove == 0:
            print("Player two has no possible moves, you have won")
            break

        #adjust variables accordingly
        stones -= playerTwoMove
        playerTwoCash -= playerTwoMove

        #output
        print("Player two removes", playerTwoMove, "stones")
        print("Stones left:", stones)
        print("Player one cash:", playerOneCash)
        print("player two cash:", playerTwoCash)

        
def playNimWithCash2(n, d, e, remove):

    #initiate variables
    moveTable = nimWithCashMove(n, d, e, remove)
    stones = n
    playerOneCash = d
    playerTwoCash = e
    playerOneMove = 0
    playerTwoMove = 0

    while(True):
        
        #determine the computer's move
        playerOneMove = moveTable[stones][playerOneCash][playerTwoCash]

        #no possible moves
        if playerOneMove == 0:
            print("Player one has no possible moves, you have won")
            break

        #adjust variables accordingly
        stones -= playerOneMove
        playerOneCash -= playerOneMove

        #output
        print("Player one removes", playerOneMove, "stones")
        print("Stones left:", stones)
        print("Player one cash:", playerOneCash)
        print("player two cash:", playerTwoCash)

        #determine whether computer has won
        if stones < min(remove):
            print("The computer has won")
            break
        elif playerTwoCash < min(remove):
            print("The computer has won")
            break

        #input protection
        playerTwoMove = int(input("Enter number of stones to remove: "))
        while(not playerTwoMove in remove or not playerTwoMove <= playerTwoCash or playerTwoMove > stones):
            if(not playerTwoMove in remove):
                playerTwoMove = int(input("That is not a possible number of stone to be removed, enter another value: "))
            elif(not playerTwoMove <= playerTwoCash):
                playerTwoMove = int(input("You do not have enough cash to play that move, enter another value: "))
            elif(playerTwoMove > stones):
                playerTwoMove = int(input("There are not enough stones left for you to play that move, enter another value: "))

        #adjust variables accordingly
        stones -= playerTwoMove
        playerTwoCash -= playerTwoMove
        
        #reset the move
        playerTwoMove = 0

        #output
        print("Stones left:", stones)
        print("Player one cash:", playerOneCash)
        print("player two cash:", playerTwoCash)

        #determine whether player two has won
        if stones < min(remove):
            print("You have won")
            break
        elif playerOneCash < min(remove):
            print("You have won")
            break

restartOption = '3'
stones = '-1'
player1 = '-1'
player2 = '-1'
playerOption = '0'
rule = []
invalidInput = True
while True:
    
    #player chooses to change everything
    if restartOption == '3':
        invalidInput = True
        while(invalidInput):
            rules = input("Possible stones to be removed (separated by space): ")
            rules = rules.split()
            rule = []
            invalidInput = False
            for x in rules:
                if(not x.isdigit() or int(x) <= 0):
                    print(x, "is not a positive integer value")
                    invalidInput = True

        invalidInput = True            
        while(invalidInput):
            stones = input("Starting stones: ")
            invalidInput = False
            if(not stones.isdigit()):
                print(stones, "is not a non-negative integer value")
                invalidInput = True

        invalidInput = True
        while(invalidInput):
            player1 = input("Player one starting cash: ")
            invalidInput = False
            if(not player1.isdigit()):
                print(player1, "is not a non-negative integer value")
                invalidInput = True

        invalidInput = True
        while(invalidInput):
            player2 = input("Player Two starting cash: ")
            invalidInput = False
            if(not player2.isdigit()):
                print(player2, "is not a non-negative integer value")
                invalidInput = True

        invalidInput = True
        while(invalidInput):
            playerOption = input("Which player would you like to play as (1 or 2): ")
            invalidInput = False
            if(playerOption != "1" and playerOption != "2"):
                print("Input must be either '1' or '2'")
                invalidInput = True

        #convert all inputs into numeric values
        rules = list(dict.fromkeys(rules))
        for x in rules:
            rule.append(int(x))
        stones = int(stones)
        player1 = int(player1)
        player2 = int(player2)

    #player chooses to change starting cash of both players
    elif restartOption == '2':
        
        invalidInput = True
        while(invalidInput):
            player1 = input("Player one starting cash: ")
            invalidInput = False
            if(not player1.isdigit()):
                print(player1, "is not a non-negative integer value")
                invalidInput = True

        invalidInput = True
        while(invalidInput):
            player2 = input("Player Two starting cash: ")
            invalidInput = False
            if(not player2.isdigit()):
                print(player2, "is not a non-negative integer value")
                invalidInput = True
                
        player1 = int(player1)
        player2 = int(player2)
        
    if playerOption == '1':
        playNimWithCash1(stones, player1, player2, rule)
    elif playerOption == '2':
        playNimWithCash2(stones, player1, player2, rule)
        
    invalidInput = True
    while(invalidInput):
        restartOption = input("Enter (1) to keep the same rules, (2) to change starting cash, (3) to change everything, (nothing) to exit game: ")
        invalidInput = False
        if(restartOption != "1" and restartOption != "2" and restartOption != "3"):
            print("Input must be either '1', '2', or '3'")
            invalidInput = True
    if(restartOption == ""):
        break
