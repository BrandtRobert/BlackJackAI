from src.Deck import BlackJackDeck
from src.Dealer import BlackJackDealer
from src.Player import Player

class BlackJackGame:

    def __init__(self, numberOfPlayers):
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
        fself.player.hand.append(self.deck.drawCard())
         # deal second card to dealer
        dealerFaceCard = self.dealer.hand.append(self.deck.drawCard())
        # keep track of the card that is face up on the dealer so the player knows what to base their moves off of
        self.dealer.faceUpCard = dealerFaceCard

    def epsilonGreedy(epsilon, Q, state):
        validMoves = np.array(self.player.validMoves(state))
        if np.random.uniform() < epsilon:
            # Random Move
            return np.random.choice(validMoves)
        else:
            # Greedy Move
            Qs = np.array([Q.get((tuple(state),m), 0) for m in validMoves])
            return validMoves[ np.argmax(Qs) ]

    def getState(self):
        return tuple(self.player.hand + self.dealer.faceUpCard)

    def trainQ(self, numberGames, learningRate, epsilonDecayFactor):
        epsilon = 1.0
        epsilons = np.zeros(numberGames)
        numberSteps = np.zeros(numberGames)
        Q = {}


        for nGames in range(numberGames):
            epsilon *= epsilonDecayFactor
            epsilons[nGames] = epsilon
            step = 0
            self.deal()
            done = False

            while not done:
                step += 1
                state = self.getState()
                move = epsilonGreedy(epsilon, Q, state)
                playerCardCount = self.player.makeMove(move, self.deck)
                newState = self.getState()

                if (tuple(state + (move, ))) not in Q:
                    Q[tuple(state + (move, ))] = 0

                if move == 'stay':
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
        
