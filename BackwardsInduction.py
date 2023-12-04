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
    
    myGameTree = buildTreeRecurse(startGame, 10)
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
                #print(currPlayer.getHandValue())
                knockHandValues[currPlayer.getHandValue()] += 1
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
         


def buildTreeRecurse(currentGameState, depthAllowedLeft):
    #Base cases: player has blitz, person knocked and has returned to them
    currNode = GameStateNode(currentGameState)
    #print(currNode.gameState.getPlayers()[0].getHandValue())
    #print(currNode.gameState.getPlayers()[1].getHandValue())
    #print(" ")
    
    currPlayer = currentGameState.getPlayers()[currentGameState.getCurrentPlayerIDX()]
    if (depthAllowedLeft == 0):
        return currNode
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
        currNode.knockChild = buildTreeRecurse(gameAfterKnock, depthAllowedLeft - 1) 
        
    #If deck is empty, we need to reshuffle discard pile into the deck again
    if (currentGameState.getDeckSize() == 0):
        currentGameState.reshuffleDeck()
            
    gameAfterDraw = currentGameState.copySelf()
    gameAfterDraw.drawCardActivePlayer()
    gameAfterDraw.advanceActivePlayerIDX()
    
    currNode.drawChild = buildTreeRecurse(gameAfterDraw, depthAllowedLeft - 1)
    
    gameAfterPickDiscard = currentGameState.copySelf()
    gameAfterPickDiscard.pickDicardCardActivePlayer()
    gameAfterPickDiscard.advanceActivePlayerIDX()
    
    currNode.pickDiscardChild = buildTreeRecurse(gameAfterPickDiscard, depthAllowedLeft - 1)    
    
    return currNode

knockHandValues = [0] * 32
#print(backInduction())

sumOutcomes = [0,0]    
for i in range(30):
    currOutcome = backInduction()
    sumOutcomes[0] += currOutcome[0]
    sumOutcomes[1] += currOutcome[1]
print(sumOutcomes)

y = knockHandValues
x = list(range(32))

fig,ax= plt.subplots()
ax.scatter(x,y)
ax.set(xlim=(0,32),ylim=(0,1000))
plt.show()