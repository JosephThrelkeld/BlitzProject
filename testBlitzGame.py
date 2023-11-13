from BlitzGameLogic import *
import unittest

class TestCalcHandValue(unittest.TestCase): 
    def test_AllDiffSuits(self):
        card2Spades = Card(Symbols.TWO, Suits.SPADES)
        card2Clubs = Card(Symbols.TWO, Suits.CLUBS)
        card2Hearts = Card(Symbols.TWO, Suits.HEARTS)
        
        cardAceDiamonds = Card(Symbols.ACE, Suits.DIAMONDS)
        cardJackSpades = Card(Symbols.JACK, Suits.SPADES)
        
        self.assertEqual(BlitzGame.calcHandValue([card2Clubs,card2Hearts,card2Spades]), 2)
        self.assertEqual(BlitzGame.calcHandValue([cardAceDiamonds,cardJackSpades,card2Clubs]), 11)
        self.assertEqual(BlitzGame.calcHandValue([cardJackSpades,card2Hearts,cardAceDiamonds]), 11)
    
    def test_TwoSameSuit(self):
        card2Spades = Card(Symbols.TWO, Suits.SPADES)
        card2Clubs = Card(Symbols.TWO, Suits.CLUBS)
        card2Hearts = Card(Symbols.TWO, Suits.HEARTS)
        
        cardAceDiamonds = Card(Symbols.ACE, Suits.DIAMONDS)
        cardJackSpades = Card(Symbols.JACK, Suits.SPADES)
        cardQueenSpades = Card(Symbols.QUEEN, Suits.SPADES)

        self.assertEqual(BlitzGame.calcHandValue([card2Clubs,card2Clubs,card2Spades]), 4)
        self.assertEqual(BlitzGame.calcHandValue([cardAceDiamonds,cardAceDiamonds,card2Clubs]), 12)
        self.assertEqual(BlitzGame.calcHandValue([cardJackSpades,cardQueenSpades,card2Hearts]), 20)
        
    def test_allSameSuit(self):
        card2Spades = Card(Symbols.TWO, Suits.SPADES)
        
        card9Diamonds = Card(Symbols.NINE, Suits.DIAMONDS)
        cardAceDiamonds = Card(Symbols.ACE, Suits.DIAMONDS)
        cardJackSpades = Card(Symbols.JACK, Suits.SPADES)
        cardQueenSpades = Card(Symbols.QUEEN, Suits.SPADES)
        cardAceSpades = Card(Symbols.ACE, Suits.SPADES)

        self.assertEqual(BlitzGame.calcHandValue([card2Spades,cardQueenSpades,cardJackSpades]), 22)
        self.assertEqual(BlitzGame.calcHandValue([cardAceDiamonds,cardAceDiamonds,card9Diamonds]), 21)
        self.assertEqual(BlitzGame.calcHandValue([cardJackSpades,cardQueenSpades,cardAceSpades]), 31)

unittest.main(verbosity=3)