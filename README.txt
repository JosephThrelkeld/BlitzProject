Code towards project of simulating and analyzing game of blitz




Blitz is a card game played by two or more people and with a deck consisting of two standard
playing card decks (minus the jokers).

The goal of the game is to be the last one remaining.

Each player starts the game with three chips, and each time they lose, they lose a chip.
When they lose a round when they have no chips left they lose.

The players play the game in a circle.



Rounds
Each round consists of four phases:
    Set up: The dealer collects all cards in the blitz deck, shuffles, and then deals three cards face down 
    to each player.
    
    Hand Refinement: The dealer turns over the first card of the remaining deck to start a face up pile. The
    dealer passes the deck and the face up pile to their right. 
        Each player who is passed to starts their 'turn' which consists of:
            Drawing from either pile and putting down a card from their hand or knocking
            Pasing the face up pile and deck to the next person.
        Players who knock, can't take anything from either pile
        If a player knocks, we progress to the next phase.
    
    Last Chance: After a player knocks (and takes no card from either pile), Each player takes one last
    turn and when the two piles return to the player who knocks, each player reveals their hand and all
    players tied for the lowest hand value lose and put in a chip, or lose if they have no chips to put in.

SPECIAL RULE: If any player at any point has a hand value of 31, they immediately call 'blitz!' and reveal the
cards. When they do, each other player loses the round simultaneously and instantaneously, and the round is 
ended.




Hand Values
The value of each player's hand is calculated by finding the maximum value found from adding up all the card 
values of each card in the same suit. 
Card values are as printed except for aces and face cards. Face cards are always worth 10 and the first ace of
a suit is worth 11 while the second in the same suit is worth 1.

For example, the blitz hand value of 31 is only reachable with 2 face cards and an ace that all share a suit.
A hand with cards that are of all different suits would take the value of the highest card present.




The code contained inside of this repository will assist in the analysis and simulation of this game.