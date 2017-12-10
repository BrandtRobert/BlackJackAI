import copy


class BlackJackDealer:
    def __init__(self):
        self.hand = []

    def clearHand(self):
        self.hand = []

    def dealerValidMoves(self, state):
        validMove = ''
        totalCardCount = 0

        # calculate the running count for the cards in state
        for card in state:
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

        return validMove


    def makeMove(self, state, move, currentDeck):
        postMoveState = copy.copy(state)

        # if hit, then pop a card off the running deck and add it to the returned state.
        # if the move is stay, then just return the deck that is passed in.
        if move == "hit":
            nextCard = currentDeck.pop()
            postMoveState.append(nextCard)

        return postMoveState