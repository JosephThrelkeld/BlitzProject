from BlitzGameLogic import *
import matplotlib.pyplot as plt
import copy

class GameStateNode:    
    def __init__(self, gameStateIn):
        self.drawChild = None
        self.pickDiscardChild = None
        self.knockChild = None
        self.gameState = gameStateIn
        



#Using recursion to build game tree and copies of BlitzGame to store game state
def backInduction():
    startGame = BlitzGame(2)
    startGame.setupRound()
    
    myGameTree = buildTreeRecurse(startGame, 0, 1)

    return backtrackRecurse(myGameTree)
    

def backtrackRecurse(currNode):
    currPlayerIDX = currNode.gameState.getCurrentPlayerIDX()
    currPlayer = currNode.gameState.getPlayers()[currPlayerIDX]
    if currNode.drawChild == None and currNode.pickDiscardChild == None and currNode.knockChild == None:
        if currNode.gameState.getPlayers()[0].getHandValue() == currNode.gameState.getPlayers()[1].getHandValue():
            if currNode.gameState.getPlayers()[0].getHandValue() == 31:
                raise Exception("This should not be possible")
            return [0,0]
        if currNode.gameState.getPlayers()[0].getHandValue() > currNode.gameState.getPlayers()[1].getHandValue():
            return [1,-1]
        else:
            return [-1,1]
    else:
        resultsArr = []
        if currNode.knockChild != None:
            resultsArr.append(backtrackRecurse(currNode.knockChild))
            if (resultsArr[-1][currPlayerIDX] == 1):
                knockHandValues[currPlayer.getHandValue()] += 1
            else:
                noKnockHandValues[currPlayer.getHandValue()] += 1
        if currNode.drawChild != None:
            resultsArr.append(backtrackRecurse(currNode.drawChild))
        if currNode.pickDiscardChild != None:
            resultsArr.append(backtrackRecurse(currNode.pickDiscardChild))
        
        
        maxResult = [-2,-2]
        for result in resultsArr:
            if result[currPlayerIDX] > maxResult[currPlayerIDX]:
                maxResult = result
        if maxResult == [-2,-2]:
            raise Exception("Assignment of maxResult was supposed to happen")
       
        return maxResult
         


def buildTreeRecurse(currentGameState, pickDiscardTimes, numRounds):
    #Base cases: player has blitz, person knocked and has returned to them
    currNode = GameStateNode(currentGameState)


    addRound = currentGameState.getCurrentPlayerIDX() == 1 #If we are at end of player order (player 1) we need to add 1 to the round 
    if (numRounds == 5):
        return currNode
    if (numRounds > 5):
        raise Exception("This shouldn't happen")
    if (currentGameState.getPlayers()[0].getHandValue() == 31 or currentGameState.getPlayers()[1].getHandValue() == 31):
        return currNode
    if (currentGameState.getPlayerKnocked()):
        if (currentGameState.getTurnsLeft() < 0):
            raise Exception("turns are supposed to be set to >=0 if a player has knocked")
        elif (currentGameState.getTurnsLeft() == 0):
            return currNode
        else:
            currentGameState.decrementTurnsLeft()
    else:
        gameAfterKnock = currentGameState.copySelf()
        gameAfterKnock.playerKnocks()
        gameAfterKnock.advanceActivePlayerIDX()
        currNode.knockChild = buildTreeRecurse(gameAfterKnock, 0, numRounds + addRound) 
        
    #If deck is empty, we need to reshuffle discard pile into the deck again
    if (currentGameState.getDeckSize() == 0):
        currentGameState.reshuffleDeck()
    
    startingHandVal = currentGameState.getPlayers()[currentGameState.getCurrentPlayerIDX()].getHandValue()
    gameAfterDraw = currentGameState.copySelf()
    handValIncrease = gameAfterDraw.drawCardActivePlayer()
    gameAfterDraw.advanceActivePlayerIDX()
    currentGameState.getPlayers()
    drawIncreaseHandValueObs[startingHandVal].append(handValIncrease)
    currNode.drawChild = buildTreeRecurse(gameAfterDraw, 0, numRounds + addRound)
    
    if pickDiscardTimes < 2:
        gameAfterPickDiscard = currentGameState.copySelf()
        gameAfterPickDiscard.pickDicardCardActivePlayer()
        gameAfterPickDiscard.advanceActivePlayerIDX()
        
        currNode.pickDiscardChild = buildTreeRecurse(gameAfterPickDiscard, pickDiscardTimes + 1, numRounds + addRound)    
    
    return currNode


#Keeping track of how many times each option is present and when it is or is not advantageous
#Not keeping track of when results are [0,0] as it indicates unfinished path. 
knockHandValues = [0] * 32
noKnockHandValues = [0] * 32

drawIncreaseHandValueObs = [[] for i in range(32)]

knockPercentValues = [0] * 32



sumOutcomes = [0,0]    
for i in range(1000):
    print(i)
    currOutcome = backInduction()
    if (currOutcome[0] == 1):
        sumOutcomes[0] += 1
    elif currOutcome[1] == 1:
        sumOutcomes[1] += 1


for i in range(len(knockPercentValues)):
    if (knockHandValues[i] + noKnockHandValues[i]) != 0:
        knockPercentValues[i] = (knockHandValues[i] / (knockHandValues[i] + noKnockHandValues[i])) * 100

drawIncreaseHandValueAves = [0] * 32
for i in range(len(drawIncreaseHandValueObs)):
    if len(drawIncreaseHandValueObs[i]) != 0:
        drawIncreaseHandValueAves[i] = sum(drawIncreaseHandValueObs[i]) / len(drawIncreaseHandValueObs[i])

print(sumOutcomes)



x = list(range(32))

y1 = knockHandValues
y2 = knockPercentValues
y3 = drawIncreaseHandValueAves

fig,ax= plt.subplots()
ax.bar(x,y2)
ax.set(xlim=(0,32),ylim=(0,100))
ax.set_ylabel("Percent")
ax.set_xlabel("Hand Value")
ax.set_title("Percent of Knock Children that lead to Positive Payoff Values\n 1000 tests, maximum depth of 5 rounds")

plt.show()