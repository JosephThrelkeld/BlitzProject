from BlitzGameLogic import *
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
    myGameTree = buildTreeRecurse(startGame)
    return myGameTree



def buildTreeRecurse(currentGameState):
    #Base cases: player has blitz, person knocked and has returned to them
    currNode = GameStateNode(currentGameState)
    
    currPlayer = currentGameState.getPlayers()[currentGameState.getCurrentPlayerIDX()]
    if (currPlayer.getHandValue() == 31):
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
        currNode.knockChild = buildTreeRecurse(gameAfterKnock) 
        
    #If deck is empty, we need to reshuffle discard pile into the deck again
    if (currentGameState.getDeckSize() == 0):
        currentGameState.reshuffleDeck()
            
    gameAfterDraw = currentGameState.copySelf()
    gameAfterDraw.drawCardActivePlayer()
    gameAfterDraw.advanceActivePlayerIDX()
    
    currNode.drawChild = buildTreeRecurse(gameAfterDraw)
    
    gameAfterPickDiscard = currentGameState.copySelf()
    gameAfterPickDiscard.pickDicardCardActivePlayer()
    gameAfterPickDiscard.advanceActivePlayerIDX()
    
    currNode.pickDiscardChild = buildTreeRecurse(gameAfterPickDiscard)    
    
    return currNode
        
        
print(backInduction())