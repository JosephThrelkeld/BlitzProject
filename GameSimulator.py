import random
suitSet = {"Spades","Clubs","Hearts","Diamonds"}
cardSymbolValDict = {
    "2":2,
    "3":3,
    "4":4,
    "5":5,
    "6":6,
    "7":7,
    "8":8,
    "9":9,
    "10":10,
    "J":10,
    "Q":10,
    "K":10,
    "A":11
}

def buildDeck():
    deck = []
    for suit in suitSet:
        for key in cardSymbolValDict:
            deck.append([key, suit])
    return deck

def calcAveHandValue(num):
    random.seed()

    deck = buildDeck()
    blitzDeck = 2 * deck
    
    handValueCount = [0] * 32
    for i in range(num):
        random.shuffle(blitzDeck)
        suitValues = [0,0,0,0] #Spades, Clubs, Hearts, Diamonds
        aceSeen = [False,False,False,False] #Spades, Clubs, Hearts, Diamonds
        for i in range(3):
            if (blitzDeck[i][1] == "Spades"):
                if (blitzDeck[i][0] == "A"):
                    if (aceSeen[0]):
                        suitValues[0] += 1
                    else:
                        suitValues[0] += 11
                        aceSeen[0] = True
                else:
                    suitValues[0] += cardSymbolValDict[blitzDeck[i][0]]
            elif (blitzDeck[i][1] == "Clubs"):
                if (blitzDeck[i][0] == "A"):
                    if (aceSeen[1]):
                        suitValues[1] += 1
                    else:
                        suitValues[1] += 11
                        aceSeen[1] = True
                else:
                    suitValues[1] += cardSymbolValDict[blitzDeck[i][0]]
            elif (blitzDeck[i][1] == "Hearts"):
                if (blitzDeck[i][0] == "A"):
                    if (aceSeen[2]):
                        suitValues[2] += 1
                    else:
                        suitValues[2] += 11
                        aceSeen[2] = True
                else:
                    suitValues[2] += cardSymbolValDict[blitzDeck[i][0]] 
            elif (blitzDeck[i][1] == "Diamonds"):
                if (blitzDeck[i][0] == "A"):
                    if (aceSeen[3]):
                        suitValues[3] += 1
                    else:
                        suitValues[3] += 11
                        aceSeen[3] = True
                else:
                    suitValues[3] += cardSymbolValDict[blitzDeck[i][0]] 
        handValueCount[max(suitValues)] += 1
    
    sum = 0
    for hvCount in handValueCount:
        sum += hvCount
    aveValue = 0
    for i in range(len(handValueCount)):
        if (i != 0):
            aveValue += handValueCount[i]/sum * i
    return aveValue 

def aveValueAdd(num):
    random.seed()

    deck = buildDeck()
    blitzDeck = 2 * deck

    for i in range(num):
        random.shuffle(blitzDeck)
        suitValues = [0,0,0,0] #Spades, Clubs, Hearts, Diamonds
        aceSeen = [False,False,False,False] #Spades, Clubs, Hearts, Diamonds
        for i in range(3):
            if (blitzDeck[i][1] == "Spades"):
                if (blitzDeck[i][0] == "A"):
                    if (aceSeen[0]):
                        suitValues[0] += 1
                    else:
                        suitValues[0] += 11
                        aceSeen[0] = True
                else:
                    suitValues[0] += cardSymbolValDict[blitzDeck[i][0]]
            elif (blitzDeck[i][1] == "Clubs"):
                if (blitzDeck[i][0] == "A"):
                    if (aceSeen[1]):
                        suitValues[1] += 1
                    else:
                        suitValues[1] += 11
                        aceSeen[1] = True
                else:
                    suitValues[1] += cardSymbolValDict[blitzDeck[i][0]]
            elif (blitzDeck[i][1] == "Hearts"):
                if (blitzDeck[i][0] == "A"):
                    if (aceSeen[2]):
                        suitValues[2] += 1
                    else:
                        suitValues[2] += 11
                        aceSeen[2] = True
                else:
                    suitValues[2] += cardSymbolValDict[blitzDeck[i][0]] 
            elif (blitzDeck[i][1] == "Diamonds"):
                if (blitzDeck[i][0] == "A"):
                    if (aceSeen[3]):
                        suitValues[3] += 1
                    else:
                        suitValues[3] += 11
                        aceSeen[3] = True
                else:
                    suitValues[3] += cardSymbolValDict[blitzDeck[i][0]] 



print(calcAveHandValue(10000))