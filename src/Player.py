# Implements a Player
#   A Player has a hand, and they also have a set of valid moves they can make
#   Author: Courtney Schulze

import copy

class Player:
    #creates a new Player and gives them an empty hand
    def __init__ (self):
        self.hand = []
        self.cardCount = 0
        #these are the first two cards that the Player gets that makes up the state
        self.initialCards = []

    #Starts a new hand for the Player and clears card count
    def clearHand(self):
        self.hand = []
        self.cardCount = 0

    #Deals a card from the deck into the Player's hand
    def hit(self, deck):
        card = deck.drawCard()
        cardVal = card[0]
        self.hand += card
        if (len(hand) < 2):
            self.initialCards += card

        #add card value to the player's total card count
        if cardVal == 'A':
            self.cardCount += 11
        elif cardVal = 'J' or cardVal = 'Q' or cardVal = 'K'
            self.cardCount += 10
        else:
            self.cardCount += cardVal

    #Defines the valid moves a player can make
    #A player can always stand, or they can hit if their card count is less than 21
    def validMoves(self):
        validMoves = ['stand']
        if (self.cardCount < 21):
            validMoves.append('hit')

        return validMoves

    def makeMove(self, move, currentDeck):


    #
