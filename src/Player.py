# Implements a Player
#   A Player has a hand, and they also have a set of valid moves they can make
#   Author: Courtney Schulze

import copy
# from src.Deck import BlackJackDeck
from Deck import BlackJackDeck

class Player:
    #creates a new Player and gives them an empty hand
    def __init__ (self):
        self.hand = []
        self.cardCount = 0
        self.bust = False

    #Starts a new hand for the Player and clears card count
    def clearHand(self):
        self.hand = []
        self.cardCount = 0
        self.bust = False

    def getCardCount(self):
        count = 0
        nonAces = [m for m in self.hand if m != 'A']
        aces = [m for m in self.hand if m == 'A']
        # Sum all the 'regular' cards
        for card in nonAces:
            if card is 'J' or card is 'Q' or card is 'K':
                count += 10
            else:
                count += card
        # If adding an ace as 11 would exceed 21, add the ace as 1 instead
        for card in aces:
            if count + 11 > 21:
                count += 1
            else:
                count += 11
        return count

    def addCardToHand (self, card):
        self.hand.append(card)
        # Keep the hand in sorted order with aces at the end
        nonAces = [m for m in self.hand if m != 'A']
        aces = [m for m in self.hand if m == 'A']
        self.hand = sorted(nonAces) + aces
        # Update card count
        self.cardCount = self.getCardCount()

    #Deals a card from the deck into the Player's hand
    #Returns either card value or 'bust' if card value is over 21
    def hit(self, deck):
        card = deck.drawCard()
        self.addCardToHand(card)
        if self.cardCount > 21:
            self.bust = True
        return self.hand

    #Defines the valid moves a player can make
    #A player can always stand, or they can hit if their card count is less than 21
    def validMoves(self):
        validMoves = ['stand']
        if (self.getCardCount() < 21):
            validMoves.append('hit')
            validMoves.append('double')
        return validMoves

    def makeMove(self, move, currentDeck):
        if move == 'hit' or move == 'double':
            return self.hit(currentDeck)
        else:
            return self.hand

    def getHand(self):
        return self.hand

    def getInitialHand(self):
        return self.hand[:2]

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
