import random

# Implements a BlackJackDeck
#   Looks like a standard deck of cards except for suits are ignored.
#   All face cards are represented as 10's (since for black jack this doesn't matter).
#   A new deck is shuffled by default. You can disable shuffle if you want by passing
#       deck = BlackJackDeck (shuffleCards = False)
#   You can activate suits and faces with this option
#       deck = BlackJackDeck (SuitsAndFaces = True)
#   Author: Brandt Reutimann
class BlackJackDeck:
    #Creates a new deck of shuffled cards
    def __init__ (self, shuffleCards = True, SuitsAndFaces = False):
        if (SuitsAndFaces):
            self.cards = self.newDeckFacesAndSuits(shuffleCards)
        else:
            self.cards = self.newShuffledDeck(shuffleCards)

    # Returns a new deck, without suit represenations and face cards as 10s
    def newShuffledDeck (self, shuffleCards):
        cards = []
        cards += ['A'] * 4
        for i in range(2,11):
            cards += [i] * 4
        cards += [10] * 12
        if (shuffleCards):
            random.shuffle(cards)
        return cards
    
    # Returns a new deck where each card is a tuple of it's value and suit
    # Face cards are chars: 'J', 'Q', 'K'
    # Suits are chars: 'S', 'C', 'D', 'H'
    def newDeckFacesAndSuits (self, shuffleCards):
        cards = []
        # Spades, Clubs, Diamonds, Hearts
        suits = ['S', 'C', 'D', 'H']
        # Jack, Queen, King
        faces = ['J', 'Q', 'K']
        for s in suits:
            for f in faces:
                cards += [(f, s)]
            for i in range(2,11):
                cards += [(i, s)]
            cards += [('A', s)]
        if (shuffleCards):
            random.shuffle(cards)
        return cards

    # Draws a new card from the deck
    def drawCard (self):
        return self.cards.pop()

    # Returnts the internal list
    def getDeckAsList (self):
        return self.cards

if __name__ == '__main__':
    print ("Example of drawing 10 random cards without suits or faces:")
    deck = BlackJackDeck()
    for i in range (0, 10):
        print (deck.drawCard())
    print ("Example of drawing 10 random cards with suits and faces:")
    deckSuits = BlackJackDeck(SuitsAndFaces = True)
    for i in range (0, 10):
        print (deckSuits.drawCard())