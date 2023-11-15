from collections import deque
import random
from aenum import IntEnum, NoAlias

class Suits(IntEnum):
    SPADES = 0
    CLUBS = 1
    HEARTS = 2
    DIAMONDS = 3 
class Symbols(IntEnum):
    _settings_ = NoAlias
    TWO=2
    THREE=3
    FOUR=4
    FIVE=5
    SIX=6
    SEVEN=7
    EIGHT=8
    NINE=9
    TEN=10
    JACK=10
    QUEEN=10
    KING=10
    ACE=11

class Card:
    __symbol = -1
    __suit = -1
    def getSymbol(self):
        return self.__symbol
    def getSuit(self):
        return self.__suit
    def __init__(self, symbolIn, suitIn):
        self.__symbol = symbolIn
        self.__suit = suitIn

class Player:
    __hand = []
    __chips = 0
    def __init__(self):
        chips = 3
    def setHand(self, cardList):
        if len(cardList) > 3:
            raise Exception("Too many cards to put in hand")
        self.__hand = cardList
    def getChips(self):
        return self.__chips
    
    #For debugging and testing
    def getHandCards(self):
        handList = []
        for card in self.__hand:
            handList.append([card.getSymbol(), card.getSuit()])
        return handList
    def getHandValue(self):
        return BlitzGame.calcHandValue(self.__hand)
    #For drawing new cards with a full hand, preserves strongest three card hand out of original hand and new card
    #Returns a card to allow blitzgame to put card in discard pile
    #Discards card that isn't part of one of the potential max hands. Defaults to lowest card value and lowest suit value (as defined by enum: SPADES=0 CLUBS=1 ...)
    def drawDiscard(self, card):
        maxHand = []
        max = 0
        
        cardToRemove = -1
        ogHand = self.__hand
        for i in range(4):
                
            potentialHand = self.__hand + [card]
            cardLeftOut = potentialHand[i]
            del potentialHand[i]
            
            #Could be one if statement but would be unreadable
            if BlitzGame.calcHandValue(potentialHand) > max:
                maxHand = potentialHand
                max = BlitzGame.calcHandValue(maxHand)
                cardToRemove = cardLeftOut
            elif BlitzGame.calcHandValue(potentialHand) == max and (cardLeftOut.getSymbol() < cardToRemove.getSymbol() or cardLeftOut.getSuit() < cardToRemove.getSuit()):
                maxHand = potentialHand
                max = BlitzGame.calcHandValue(maxHand)
                cardToRemove = cardLeftOut
    
        self.__hand = maxHand
        a = BlitzGame.calcHandValue(self.__hand)
        b = BlitzGame.calcHandValue(ogHand)
        if (len(self.__hand) != 3):
            raise Exception("Hand does not have three cards in it")
        return cardToRemove
            

            



class BlitzGame:
    __deck = deque([])
    __discardPile = deque([])
    __players = []
    __playerKnocked = False
    __roundActive = False
    #Setting apart player list and playerOrder list to allow latter to only store players who haven't lost in full game sim
    __currentPlayerIDX = -1
    
    #Putting hand value calculation in blitz game class for testing and stat gathering without having to use player hands
    @classmethod
    def calcHandValue(self, handList):
        if (len(handList) != 3):
            raise ValueError("Wrong number of cards in hand")
        suitCardValList = [[],[],[],[]]
        for i in range(len(handList)):
            if 11 in suitCardValList[handList[i].getSuit()] and handList[i].getSymbol() == 11: #If current card is the second ace in getSuit(), it is worth 1 not 11.
                suitCardValList[handList[i].getSuit()].append(1) #Creating seperate enum just for second ace seems unneccessarry for now, just using 1.
            else:
                suitCardValList[handList[i].getSuit()].append(handList[i].getSymbol())
        return max(sum(suitCardValList[0]),sum(suitCardValList[1]),sum(suitCardValList[2]),sum(suitCardValList[3]))
    
    def __init__(self, numPlayers):
        self.__setDeck()
        for i in range(numPlayers):
            self.__players.append(Player())
    def __setDeck(self):
        self.__deck = deque([])
        for i in range(2):
            for suit in Suits:
                for symbol in Symbols:
                    self.__deck.append(Card(symbol, suit))
    def getPlayerHandCards(self):
        playerHands = []
        for player in self.__players:
            playerHands.append(player.getHandCards())
        return playerHands
    def getPlayerHandValues(self):
        valueList = []
        for player in self.__players:
            valueList.append(player.getHandValue())
        return valueList
    def getTopCardValDiscardPile(self):
        return self.__discardPile[0].getSymbol()
    def __shuffleDeck(self):
        random.seed()
        random.shuffle(self.__deck)
    def dealHand(self, player, cardHand):
        player.setHand(cardHand)
    def setupRound(self):
        self.__currentPlayerIDX = 0
        self.__setDeck()
        self.__discardPile = deque([])
        self.__roundActive = False
        self.__shuffleDeck()
        for player in self.__players:
            handInsert = []
            for i in range(3):
                handInsert.append(self.__deck.popleft())
            self.dealHand(player, handInsert)
        self.__discardPile.appendleft(self.__deck.popleft())
         
    #Seperating setup round and run round to allow for easy collection of statistics about starting states of rounds         
    def runRoud(self, timeLimit): #Time limit defines extra rounds apart from the first (for now)
        self.__roundActive = True
        while self.__roundActive:
            #print(self.getPlayerHandCards())
            #print(self.getPlayerHandValues())
            
            discardCard = self.__players[self.__currentPlayerIDX].drawDiscard(self.__deck.popleft()) #TODO: have players make choice between drawing from different piles and knocking 
            self.__discardPile.appendleft(discardCard)
            
            
            if self.__currentPlayerIDX == len(self.__players) - 1:
                self.__currentPlayerIDX = 0
            else:
                self.__currentPlayerIDX += 1
            
            #End conditions
            #Using time limit to stop rounds artificially for testing and collection of stats. Time limit set to -1 indicates indefinite loop    
            if timeLimit > -1:
                if timeLimit == 0:
                    self.__roundActive = False
                timeLimit -= 1
            #Ending when no deck is left 
            if len(self.__deck) == 0:
                self.__roundActive = False
        
            
    
    def runGame(self):
        None #TODO: create game loop
