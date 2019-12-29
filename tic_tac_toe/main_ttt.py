from ttt import TicTacToe,AutoPlayer,HumanPlayer
from pprint import pprint
import operator



game = TicTacToe()

a1 = AutoPlayer(symb=1,greedy=True)
a2 = AutoPlayer(symb=2,epsilon=0.2,step_size=0.4)
h1 = HumanPlayer(symb=1)

game.play(a1,a2,iter=40000)

a1.setGreedy(False)
a1.setEpsilon(0.1)
a2.setStepSize(0.2)
game.play(a1,a2,iter=40000)

a1.setGreedy(True)
a2.setStepSize(0.1)
game.play(a1,a2,iter=40000)

#print('---- LIVE GAME ------')
game.reset_board()
a2.setGreedy(True)
game.play(h1, a2, iter=1, stats=False, printBoard=True)
