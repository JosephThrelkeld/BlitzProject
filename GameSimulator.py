import random
from BlitzGameLogic import *
from aenum import IntEnum, NoAlias

#This file will use BlitzGame logic and sim to calculate statistics. Game logic will be centralized in BlitzGame and stats making will be in this file

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
    testGame = BlitzGame(1)
    handValueCount = [0] * 32
    for i in range(num):
        testGame.setupRound()
        handVal = testGame.getPlayerHandValues()[0]
        handValueCount[handVal] += 1
        
    return calcAveOfValList(handValueCount) 

def calcAverageIncreaseFromDraw(num):
    testGame = BlitzGame(1)
    handValueIncreaseCount = [0] * 32
    for i in range(num):
        testGame.setupRound()
        handVal = testGame.getPlayerHandValues()[0]
        testGame.runRoud(0)
        handValAfterDraw = testGame.getPlayerHandValues()[0]
        
        if (handValAfterDraw - handVal < 0):
            raise Exception("Hand value got worse after drawing new card")
        
        handValueIncreaseCount[handValAfterDraw - handVal] += 1

    return calcAveOfValList(handValueIncreaseCount)

#print(calcAveHandValue(10000))
print(calcAverageIncreaseFromDraw(10000)) 