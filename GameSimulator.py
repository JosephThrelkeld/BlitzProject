import random
from enum import IntEnum

#Using Enums for suits and symbols for ease of debugging
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


def buildDeck():
    deck = []
    for suit in Suits:
        for symbol in Symbols:
            deck.append([symbol, suit])
    return deck

def calcHandValue(cards):
    if (len(cards) < 3):
        raise Exception("Not enough cards")
    suitCardValList = [[],[],[],[]]  
    
    for i in range(len(cards)):
        if 11 in suitCardValList[cards[i][1]] and cards[i][0] == 11: #If current card is the second ace, it is worth 1 not 11.
            suitCardValList[cards[i][1]].append(1)
        else:
            suitCardValList[cards[i][1]].append(cards[i][0])
    
    return max([sum(suitCardValList[0]),sum(suitCardValList[1]),sum(suitCardValList[2]),sum(suitCardValList[3])])

#Calculating best three cards from a four card hand, to calculate EV of hand after a draw
def best3CardHandFrom4(list):
    return max(calcHandValue(list[:3]),calcHandValue(list[1:4]),calcHandValue([list[0],list[1],list[3]]),calcHandValue([list[0],list[2],list[3]]))

def calcAveOfValList(list):
    sum = 0
    for val in list:
        sum += val
    aveValue = 0
    for i in range(len(list)):
        if (i != 0):
            aveValue += (list[i]/sum) * i
    return aveValue 

def calcAveHandValue(num): 
    random.seed()
    deck = buildDeck()
    blitzDeck = 2 * deck

    handValueCount = [0] * 32
    for i in range(num):
        random.shuffle(blitzDeck)
        max([calcHandValue(blitzDeck[:3])])
        handValueCount[calcHandValue(blitzDeck[:3])] += 1 
    
    return calcAveOfValList(handValueCount) 

        
def aveIncreaseFromDrawing(num):
    random.seed()

    deck = buildDeck()
    blitzDeck = 2 * deck
    handValueIncreaseCount = [0] * 32

    for i in range(num):
        random.shuffle(blitzDeck)
        handValueIncreaseCount[(best3CardHandFrom4(blitzDeck[:4]) - calcHandValue(blitzDeck[:3]))] += 1

    return calcAveOfValList(handValueIncreaseCount)      



print(calcAveHandValue(10000))
print(aveIncreaseFromDrawing(10000))