from src.Deck import BlackJackDeck
from src.Dealer import BlackJackDealer
from src.Player import Player
# from Deck import BlackJackDeck
# from Dealer import BlackJackDealer
# from Player import Player
import numpy as np
import time

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
        self.player.addCardToHand(self.deck.drawCard())
        # deal first card to dealer
        self.dealer.hand.append(self.deck.drawCard())
        # deal second card to each player
        self.player.addCardToHand(self.deck.drawCard())
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
            Qs = np.array([Q.get(self.getQTuple(state, m), 0) for m in validMoves])
            moves = self.player.validMoves()
            best = moves [np.argmax(Qs)]
            return moves [np.argmax(Qs)]

    def getState(self):
        return tuple(self.player.hand + [self.dealer.faceUpCard])

    # Represent Qtable index as the sum of cards in the players hand,
    # Followed by a list of aces the players have, the dealer's up card and the move they made
    #   Ex: state = (10, 3,'A','10', hit')
    #       qTup returns (13, 'A', hit)
    def getQTuple (self, state, move):
        playerHand = state[:-1]
        aces = [c for c in playerHand if c == 'A']
        nonAces = [c for c in playerHand if c != 'A']
        pHandRep = [sum(nonAces)] + aces
        return tuple(pHandRep) + (state[-1],move)

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
                move = self.epsilonGreedy(epsilon, Q, state)
                playerCardCount = self.player.makeMove(move, self.deck)
                newState = self.getState()
                currStateTup = self.getQTuple(state, move)
                if currStateTup not in Q:
                    Q[currStateTup] = 0

                if self.player.bust:
                    # Player loses, negative reinforce
                    Q[currStateTup] += learningRate * (-1 - Q[currStateTup])
                    done = True
                # Once doubling down the player's turn is over
                elif move == 'double':
                    done = True
                    dealerResult = self.dealer.playTurn(self.deck, self.player)
                    # A dealer loss is a player win
                    if dealerResult == "loss":
                        # Positive reinforce win * 2 for doubling winnings
                        Q[currStateTup] = 2
                    elif dealerResult == "push":
                        # Neutral reinforce?
                        Q[currStateTup] = 0
                    else:
                        # Player loss negative reinforce
                        Q[currStateTup] += learningRate * (-2 - Q[currStateTup])
                elif move == 'stand':
                    done = True
                    dealerResult = self.dealer.playTurn(self.deck, self.player)
                    # A dealer loss is a player win
                    if dealerResult == "loss":
                        # Positive reinforce win
                        Q[currStateTup] = 1
                    elif dealerResult == "push":
                        # Neutral reinforce?
                        Q[currStateTup] = 0
                    else:
                        # Player loss negative reinforce
                        Q[currStateTup] += learningRate * (-1 - Q[currStateTup])

                if step > 1:
                    oldStateTup = self.getQTuple(oldState, oldMove)
                    Q[oldStateTup] += learningRate * (Q[currStateTup] - Q[oldStateTup])

                oldState, oldMove = state, move
                state = newState
        return Q

    # Implement hotstreak betting
    def determineBet (self, consecutiveWins, minBet = 5, streakFactor = 1.2, hotstreak = True):
        if hotstreak is False:
            return minBet
        return round(minBet ** streakFactor) if consecutiveWins > 0 else minBet
        
    # Test's the Q function by playing a number of games and calculating the win percentage
    def testQ (self, Q, numGames = 10000, verbose = False, esp = 0, hotstreak = False):
        # Get a new deck
        self.deck = []
        numWins = 0
        numTies = 0
        earnings = 0

        consecutiveWins = 0
        for n in range(numGames):
            self.player.clearHand()
            self.dealer.clearHand()
            self.deal()
            gameOver = False
            bet = self.determineBet(consecutiveWins, hotstreak = hotstreak)
            
            while not gameOver:
                state = self.getState()
                move = self.epsilonGreedy(esp, Q, state)
                self.player.makeMove(move, self.deck)
                if self.player.bust:
                    gameOver = True
                    earnings -= (2*bet) if move is 'double' else bet
                    consecutiveWins = 0
                    if n % 1000 == 0 and verbose:
                            resultBet = (2*bet) if move is 'double' else bet
                            print ('Initial Hand: {}, Bet: {}, Player: {}, Dealer: {}, Result: bust'.format(self.player.getInitialHand(), resultBet, self.player.hand, self.dealer.hand))
                # Player's turn is over
                elif move == 'stand' or move == 'double':
                    gameOver = True
                    gameResult = self.dealer.playTurn(self.deck, self.player)
                    # Print out everything thousandth game
                    playerWin = 'win' if gameResult is 'loss' else 'loss'
                    playerWin = 'push' if gameResult is 'push' else playerWin
                    if playerWin is 'win':
                        numWins += 1
                        consecutiveWins += 1
                        earnings += (2*bet) if move is 'double' else bet
                    elif playerWin is 'push':
                        consecutiveWins -= 1
                        numTies += 1
                    else:
                        consecutiveWins = 0
                        earnings -= (2*bet) if move is 'double' else bet
                    if n % 1000 == 0 and verbose:
                        resultBet = (2*bet) if move is 'double' else bet
                        print ('Initial Hand: {}, Bet: {}, Player: {}, Dealer: {}, Result: {}'.format(self.player.getInitialHand(), resultBet, self.player.hand, self.dealer.hand, playerWin))
        # Return the win percentage
        return ((numWins / numGames) * 100, earnings)

if __name__ == '__main__':
    game = BlackJackGame()
    st = time.time()
    print ('Training network...')
    Q = game.trainQ(1000, .6, .99)
    et = time.time()
    print ('Training time: {0:.2f}'.format(et - st))
    print ('\nPlaying 10000 games with Q Table: \n')
    winRate, earnings = game.testQ(Q, 10000, verbose = True,hotstreak = False)
    print ('Win rate was: {}, Earnings without hotstreak: ${}\n'.format(winRate, earnings))
    winRate, earnings = game.testQ(Q, 10000, hotstreak = True)
    print ('\nWin rate was: {}, Earnings with hotstreak: ${}'.format(winRate, earnings))
    print ('\nPlaying 10000 games with random moves: \n')
    randWinRate, earnings = game.testQ(Q, 10000, esp = 1, hotstreak = False)
    print ('Win rate was: {}, Earnings: ${}'.format(randWinRate, earnings))
