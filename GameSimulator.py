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
        print("list of cards to small")
        return
    suitCardValList = [[],[],[],[]]  
    
    for i in range(len(cards)):
        if 11 in suitCardValList[cards[i][1]] and cards[i][0] == 11: #If current card is the second ace, it is worth 1 not 11.
            suitCardValList[cards[i][1]].append(1)
        else:
            suitCardValList[cards[i][1]].append(cards[i][0])

    maxHV = 0 #HV Hand Value
    maxIDX = -1
    for cardList in suitCardValList:
        if sum(cardList) > maxHV:
            maxHV = sum(cardList)
            maxIDX = suitCardValList.index(cardList)
    
    #If we are testing for best 3 of 4 cards (hand after we draw) we need to subtract lowest card val from winning suit if all four cards are in winning suit
    if (len(cards) == 4 and cards[0][1] == cards[1][1] and cards[0][1] == cards[2][1] and cards[0][1] == cards[3][1]): 
        minCard = min(suitCardValList[maxIDX])
        return maxHV - min(suitCardValList[maxIDX])
    return maxHV

def calcAveOfValList(list):
    sum = 0
    for val in list:
        sum += val
    aveValue = 0
    for i in range(len(list)):
        if (i != 0):
            aveValue += (list[i]/sum) * i
    return aveValue 

def calcAveHandValue(num,afterdraw): 
    random.seed()
    deck = buildDeck()
    blitzDeck = 2 * deck
    
    n = 3 + afterdraw #Use 4 cards for calculating hands after a draw from the deck, 3 otherwise, using afterdraw arg to control

    handValueCount = [0] * 32
    for i in range(num):
        random.shuffle(blitzDeck)
        handValueCount[calcHandValue(blitzDeck[:n])] += 1 
    
    return calcAveOfValList(handValueCount) 

        
def aveIncreaseFromDrawing(num):
    random.seed()

    deck = buildDeck()
    blitzDeck = 2 * deck
    handValueIncreaseCount = [0] * 32

    for i in range(num):
        random.shuffle(blitzDeck)
        handValueIncreaseCount[(calcHandValue(blitzDeck[:4]) - calcHandValue(blitzDeck[:3]))] += 1

    return calcAveOfValList(handValueIncreaseCount)      



print(calcAveHandValue(10000,False))
print(calcAveHandValue(10000,True))
print(aveIncreaseFromDrawing(10000))