from Deck import BlackJackDeck
from Dealer import BlackJackDealer
from Player import Player
import numpy as np

class BlackJackGame:

    def __init__(self, numberOfPlayers = 1):
        self.dealer = BlackJackDealer()
        self.deck = BlackJackDeck(True, False)
        self.player = Player()
        # self.players = []
        # self.numberOfPlayers = numberOfPlayers
        # for n in range(numberOfPlayers):
        #     self.players.add(Player())


    def deal(self):
        if self.deck == []:
            self.deck = BlackJackDeck(True, False)
        # deal first card to each player
        # for player in self.players:
        #     player.hand.append(self.deck.drawCard())
        self.player.hand.append(self.deck.drawCard())
        # deal first card to dealer
        self.dealer.hand.append(self.deck.drawCard())

        # deal second card to each player
        self.player.hand.append(self.deck.drawCard())
         # deal second card to dealer
        dealerFaceCard = self.deck.drawCard()
        self.dealer.hand.append(dealerFaceCard)
        # keep track of the card that is face up on the dealer so the player knows what to base their moves off of
        self.dealer.faceUpCard = dealerFaceCard

    def epsilonGreedy(self, epsilon, Q, state):
        validMoves = np.array(self.player.validMoves())
        if np.random.uniform() < epsilon:
            # Random Move
            return np.random.choice(validMoves)
        else:
            # Greedy Move
            Qs = np.array([Q.get((tuple(state),m), 0) for m in validMoves])
            return validMoves[ np.argmax(Qs) ]

    def getState(self):
        return tuple(self.player.hand + [self.dealer.faceUpCard])

    def trainQ(self, numberGames, learningRate, epsilonDecayFactor):
        epsilon = 1.0
        epsilons = np.zeros(numberGames)
        numberSteps = np.zeros(numberGames)
        Q = {}

        for nGames in range(numberGames):
            epsilon *= epsilonDecayFactor
            epsilons[nGames] = epsilon
            step = 0
            self.player.clearHand()
            self.dealer.clearHand()
            self.deal()
            done = False

            while not done:
                step += 1
                state = self.getState()
                print (state)
                move = self.epsilonGreedy(epsilon, Q, state)
                playerCardCount = self.player.makeMove(move, self.deck)
                newState = self.getState()

                if (tuple(state + (move, ))) not in Q:
                    Q[tuple(state + (move, ))] = 0

                if move == 'stand':
                    done = True
                    dealerResult = self.dealer.playTurn(self.deck, self.player)

                    if dealerResult == "win":
                        Q[tuple(state + (move, ))] = 1
                    elif dealerResult == "push":
                        Q[tuple(state + (move,))] = 0
                    else:
                        Q[tuple(state + (move, ))] += learningRate * (-1 - Q[tuple(state + (move, ))])

                if step > 1:
                    Q[tuple(oldState + (oldMove, ))] += learningRate * (Q[tuple(state + (move, ))] - Q[tuple(oldState + (oldMove, ))])

                oldState, oldMove = state, move
                state = newState
        
    # Test's the Q function by playing a number of games and calculating the win percentage
    def testQ (Q, numGames = 10000):
        # Get a new deck
        self.deck = []
        numWins = 0
        numTies = 0

        for n in numberGames:
            self.deal()
            gameOver = False

            while not gameOver:
                state = self.getState()
                move = epsilonGreedy(1, Q, state)       
                self.player.makeMove(move, self.deck)

                # The player is done hitting
                if move is 'stand':
                    gameResult = self.dealer.playTurn(self.deck, self.player)
                    if gameResult is 'win':
                        numWins += 1
                    if gameResult is 'push':
                        numTies += 1
                    gameOver = True
                    # Print out everything thousandth game
                    if n % 1000 == 0:
                        print ('Player: {}, Dealer: {}, Result: {}'.format(state[:-1], state[-1], gameResult))
        # Return the win percentage
        return (numberWins / numberGames) * 100

if __name__ == '__main__':
    game = BlackJackGame()
    game.trainQ(10000, .7, .999)
    winRate = game.testQ()
    print ('Win rate was: {.2f}'.format(winRate))