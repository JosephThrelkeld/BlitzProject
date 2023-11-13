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
        hand = testGame.getPlayerHandValues()
        handValueCount[hand[0]] += 1
        
    return calcAveOfValList(handValueCount) 



print(calcAveHandValue(10000))