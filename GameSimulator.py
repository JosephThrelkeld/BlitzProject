import random
from BlitzGameLogic import *
from aenum import IntEnum, NoAlias
import matplotlib.pyplot as plt

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
    handValueCount = [0 for i in range(32)]
    for i in range(num):
        testGame.setupRound()
        handVal = testGame.getPlayerHandValues()[0]
        handValueCount[handVal] += 1
        
    return calcAveOfValList(handValueCount) 

def calcAverageIncreaseFromDraw(num):
    testGame = BlitzGame(1)
    handValueIncreaseCount = [0 for i in range(32)] 
    for i in range(num):
        testGame.setupRound()
        handVal = testGame.getPlayerHandValues()[0]
        testGame.runRoud(0)
        handValAfterDraw = testGame.getPlayerHandValues()[0]
        
        if (handValAfterDraw - handVal < 0):
            raise Exception("Hand value got worse after drawing new card")
        
        handValueIncreaseCount[handValAfterDraw - handVal] += 1

    return calcAveOfValList(handValueIncreaseCount)
def calcAveHandValueGivenDiscardedCardVal(num):
    testGame = BlitzGame(1)
    #ith sublist corresponds to discarded card of i value, and values are observations of hand value
    hvVSdvArr = [[] for i in range(12)] 
    for i in range(num):
        testGame.setupRound()
        testGame.runRoud(0)
        handVal = testGame.getPlayerHandValues()[0]
        discardVal = testGame.getTopCardValDiscardPile()
        if (discardVal > handVal):
            raise Exception("Discarded card value shouldn't be higher than hand value")
        hvVSdvArr[discardVal].append(handVal)
        val = None
    aveHVgivenDVarr = []
    for i in range(len(hvVSdvArr)):
        if len(hvVSdvArr[i]) == 0:
            aveHVgivenDVarr.append(0)
        else:
            aveHVgivenDVarr.append(sum(hvVSdvArr[i])/len(hvVSdvArr[i]))
    return aveHVgivenDVarr
    
#print(calcAveHandValue(10000))
#print(calcAverageIncreaseFromDraw(10000)) 
a = calcAveHandValueGivenDiscardedCardVal(1000)
x = [1,2,3,4,5,6,7,8,9,10,11,12]
y = a

fig,ax= plt.subplots()

ax.scatter(x,y)
ax.set(xlim=(0,12),ylim=(0,32))
plt.show()
