from collections import deque
import random
from enum import IntEnum

class Suits(IntEnum):
    SPADES = 0
    CLUBS = 1
    HEARTS = 2
    DIAMONDS = 3 
class Symbols(IntEnum):
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
    symbol = -1
    suit = -1
    def __init__(self, symbolIn, suitIn):
        self.symbol = symbolIn
        self.suit = suitIn

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
    def getHandValue(self):
        return BlitzGame.calcHandValue(self.__hand)
    #For drawing new cards with a full hand, preserves strongest three card hand out of original hand and new card
    #Returns a card to allow blitzgame to put card in discard pile
    #Discards card that isn't part of max 3 card hand that is found, defaults to first 3 max card hand found first (for now).
    def drawDiscard(self, card):
        max = 0
        cardToRemove = -1
        for i in range(4):
            fourCardHand = self.__hand + [card]
            cardLeftOut = fourCardHand[i]
            del fourCardHand[i]
            if BlitzGame.calcHandValue(self.__hand) > max:
                max = BlitzGame.calcHandValue(self.__hand)
                cardToRemove = cardLeftOut
        fourCardHand = fourCardHand = self.__hand + [card]
        fourCardHand.remove(cardToRemove)
        return cardToRemove
            
        

            



class BlitzGame:
    __deck = deque([])
    __discardPile = deque([])
    __players = []
    __playerKnocked = False
    __roundActive = False
    #Setting apart player list and playerOrder list to allow latter to only store active players in the game
    __activePlayers = []
    
    #Putting hand value calculation in blitz game class for testing and stat gathering without using player hands
    @classmethod
    def calcHandValue(self, handList):
        if (len(handList) != 3):
            raise Exception("Wrong number of cards in hand")
        suitCardValList = [[],[],[],[]]
        for i in range(len(handList)):
            if 11 in suitCardValList[handList[i].suit] and handList[i].symbol == 11: #If current card is the second ace in suit, it is worth 1 not 11.
                suitCardValList[handList[i].suit].append(1)
            else:
                suitCardValList[handList[i].suit].append(handList[i].symbol)
        return max(sum(suitCardValList[0]),sum(suitCardValList[1]),sum(suitCardValList[2]),sum(suitCardValList[3]))
    
    def __setDeck(self):
        self.__deck = deque([])
        for i in range(2):
            for suit in Suits:
                for symbol in Symbols:
                    self.__deck.append(Card(symbol, suit))
    def getPlayerHandValues(self):
        valueList = []
        for player in self.__players:
            valueList.append(player.getHandValue())
        return valueList
    def __shuffleDeck(self):
        random.seed()
        random.shuffle(self.__deck)
    def dealHand(self, player, cardHand):
        player.setHand(cardHand)
    def setupRound(self):
        self.__setDeck()
        self.__roundActive = False
        self.__playersOrdered = self.__players
        self.__shuffleDeck()
        for player in self.__players:
            handInsert = []
            for i in range(3):
                handInsert.append(self.__deck.popleft())
            self.dealHand(player, handInsert)
         
    #Seperating setup round and run round to allow for easy collection of statistics about starting states of rounds         
    def runRoud(self, setRound, timeLimit):
        self.setupRound()
        while self.__roundActive:
            activePlayer = self.__activePlayers.pop()
            #TODO: have players make choice between drawing from different piles and knocking 
            discardCard = activePlayer.drawDiscard()
            
            #Using time limit to stop rounds artificially for testing and collection of stats. Time limit set to -1 indicates indefinite loop
            if timeLimit > -1:
                if timeLimit == 0:
                    self.__roundActive = False
            
    
    def runGame(self):
        None #TODO: create game loop
    def __init__(self, numPlayers):
        self.__setDeck()
        for i in range(numPlayers):
            self.__players.append(Player())


myGame = BlitzGame(3)
myGame.setupRound()
print(myGame.getPlayerHandValues())