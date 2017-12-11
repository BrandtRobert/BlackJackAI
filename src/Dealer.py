import copy

class BlackJackDealer:
    def __init__(self):
        self.hand = []
        self.faceUpCard = 0
        self.cardCount = 0
        self.bust = False


    def clearHand(self):
        self.hand = []
        self.faceUpCard = 0
        self.cardCount = 0
        self.bust = False

    def dealerValidMoves(self):
        validMove = ''
        totalCardCount = 0
        # calculate the running count for the cards in state
        for card in self.hand:
            currentCardCount = totalCardCount
            # if the card is an Ace, then check if added as 11 the total is 17 or more. Otherwise, set it equal to 1.
            if card == 'A':
                if currentCardCount + 11 <= 17:
                    card = 11
                else:
                    card = 1
            if card == 'J' or card == 'Q' or card == 'K':
                card = 10
            totalCardCount += card
        # there is only ever one valid move for the dealer. if the card total is less than or equal to 16, the dealer hits.
        # otherwise the dealer stays.
        if totalCardCount <= 16:
            validMove = "hit"
        else:
            validMove = "stay"
        
        self.cardCount = self.getCardCount()
        return validMove

    def getCardCount(self):
        count = 0
        nonAces = [m for m in self.hand if m != 'A']
        aces = [m for m in self.hand if m == 'A']
        for card in nonAces:
            if card is 'J' or card is 'Q' or card is 'K':
                count += 10
            else:
                count += card
        for card in aces:
            if count + 11 > 21:
                count += 1
            else:
                count += 11
        return count

    def makeMove(self, move, currentDeck):
        # if hit, then pop a card off the running deck and add it to the returned state.
        # if the move is stay, then just return the deck that is passed in.
        if move == "hit":
            nextCard = currentDeck.drawCard()
            self.hand.append(nextCard)
            count = self.getCardCount()
            if count > 21:
                self.bust = True

    def playTurn(self, currentDeck, player):

        validMove = self.dealerValidMoves()
        while validMove is not "stay":
            self.makeMove(validMove, currentDeck)
            validMove = self.dealerValidMoves()

        if player.bust:
            return "win"
        if self.bust:
            return "loss"
        if self.cardCount == player.getCardCount():
            return "push"
        if self.cardCount > player.getCardCount():
            return "win"
        else:
            return "loss"


if __name__ == '__main__':
    dealer = BlackJackDealer()
