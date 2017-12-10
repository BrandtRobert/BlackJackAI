# Implements a Player
#   A Player has a hand, and they also have a set of valid moves they can make
#   Author: Courtney Schulze

import copy
from src.Deck import BlackJackDeck

class Player:
    #creates a new Player and gives them an empty hand
    def __init__ (self):
        self.hand = []
        self.cardCount = 0

    #Starts a new hand for the Player and clears card count
    def clearHand(self):
        self.hand = []
        self.cardCount = 0

    #Deals a card from the deck into the Player's hand
    #Returns either card value or 'bust' if card value is over 21
    def hit(self, deck):
        card = deck.drawCard()
        if (isinstance(card, int)):
            cardVal = card
        else:
            cardVal = card[0]

        self.hand.append(card)

        #add card value to the player's total card count
        if cardVal == 'A':
            self.cardCount += 11
        elif cardVal == 'J' or cardVal == 'Q' or cardVal == 'K':
            self.cardCount += 10
        else:
            self.cardCount += cardVal

        if self.cardCount > 21:
            return 'bust'
        else:
            return self.cardCount


    #Defines the valid moves a player can make
    #A player can always stand, or they can hit if their card count is less than 21
    def validMoves(self):
        validMoves = ['stand']
        if (self.cardCount < 21):
            validMoves.append('hit')

        return validMoves

    def makeMove(self, move, currentDeck):
        if move == 'hit':
            return self.hit(currentDeck)
        else:
            return self.hand

    def getHand(self):
        return self.hand

    def getInitialHand(self):
        return self.hand[:2]

    def getCardCount(self):
        return self.cardCount

if __name__ == '__main__':
    # create both deck and player
    deck = BlackJackDeck()
    player = Player()
    #put first two cards in player's hand
    player.hit(deck)
    player.hit(deck)

    print("Here are the first two cards in the player's hand:")
    print(player.getInitialHand())
    print("Here are the valid moves the player can now make:")
    print(player.validMoves())
    print("Here's all of the cards that are now in the player's hand:")
    print(player.getHand())

    print("Keep hitting until the player busts!")
    while True:
        result = player.hit(deck)
        print("Player hits: " + str(result))
        if result == 'bust':
            break

    print("Player's hand: " + str(player.getHand()))
