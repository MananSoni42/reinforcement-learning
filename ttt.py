import random
import numpy as np
random.seed(42)
# Use a simple algo  to solve tic-tac-toe

"""
1. Generate all states
2. dict: stae -> real number
3. Algo iterational update
4. Playing interface
Machine is X always
"""

class TicTacToe(object):
    """docstring for TicTacToe."""

    graphics = {
    0: ' ',
    1: 'O',
    2: 'X'
    }

    def __init__(self,mode='train'):
        self.val = self.get_all_states()
        self.board = [(0,0,0,0,0,0,0,0,0)]
        self.mode = mode

    def valid_state(self,state):
        counto = sum([1 for x in state if x==1])
        countx = sum([1 for x in state if x==2])
        if abs(counto-countx) <= 1:
            return True
        return False

    def won(self, c, n):
        if c[0] == n and c[1] == n and c[2] == n: return True
        elif c[3] == n and c[4] == n and c[5] == n: return True
        elif c[6] == n and c[7] == n and c[8] == n: return True

        elif c[0] == n and c[3] == n and c[6] == n: return True
        elif c[1] == n and c[4] == n and c[7] == n: return True
        elif c[2] == n and c[5] == n and c[8] == n: return True

        elif c[0] == n and c[4] == n and c[8] == n: return True
        elif c[2] == n and c[4] == n and c[6] == n: return True

        else: return False

    def state_prob(self, state):
        if self.won(state,1):
            return -1.0
        elif self.won(state,2):
            return 1.0
        else:
            return 0.5

    def get_all_states(self):
        states = dict()
        for i1 in range(3):
            for i2 in range(3):
                for i3 in range(3):
                    for i4 in range(3):
                        for i5 in range(3):
                            for i6 in range(3):
                                for i7 in range(3):
                                    for i8 in range(3):
                                        for i9 in range(3):
                                            state = (i1,i2,i3,i4,i5,i6,i7,i8,i9)
                                            if self.valid_state(state):
                                                states[state] = self.state_prob(state)
        return states

    def print_state(self,state):
        print(f'\n----+---+----')
        print(f'| {TicTacToe.graphics[state[0]]} | {TicTacToe.graphics[state[1]]} | {TicTacToe.graphics[state[2]]} |')
        print(f'----+---+----')
        print(f'| {TicTacToe.graphics[state[3]]} | {TicTacToe.graphics[state[4]]} | {TicTacToe.graphics[state[5]]} |')
        print(f'----+---+----')
        print(f'| {TicTacToe.graphics[state[6]]} | {TicTacToe.graphics[state[7]]} | {TicTacToe.graphics[state[8]]} |')
        print(f'----+---+----')

    def check_play(self, hist):
        val = False
        if self.won(self.board[-1],1):
            hist.append(1)
            val = True

        elif self.won(self.board[-1],2):
            hist.append(2)
            val = True

        elif sum(self.board[-1]) in [13,14]:
            hist.append(0)
            val = True
        return hist, val

    def reset_board(self):
        self.board = [(0,0,0,0,0,0,0,0,0)]

    def get_stats(self,hist,parts=10):
        hist = np.array(hist)
        tot = np.shape(hist)[0]
        d = 100*np.where(hist==0)[0].shape[0]/tot
        w1 = 100*np.where(hist==1)[0].shape[0]/tot
        w2 = 100*np.where(hist==2)[0].shape[0]/tot
        print(f'P1: {round(w1,3)}% | P2: {round(w2,2)}% | Draw: {round(d,2)}%')
        sec_str = ''
        for i,arr in enumerate(np.array_split(hist,parts)):
            tot = np.shape(arr)[0]
            w2 = 100*np.where(arr==2)[0].shape[0]/tot
            sec_str += f'{i+1}: {round(w2,2)}% | '
        print('| ' + sec_str)

    def play(self, p1, p2, iter,stats=True,printBoard=False):
        hist = []
        for i in range(iter):
            finished = False
            self.reset_board()
            while True:
                if printBoard:
                    self.print_state(self.board[-1])

                hist, finished = self.check_play(hist)
                if finished:
                    break

                state,val = p1.move(self.board,self.val)
                self.board.append(state)

                hist, finished = self.check_play(hist)
                if finished:
                    self.val = p2.update_vals(self.board,self.val)
                    break

                state,nval = p2.move(self.board,self.val)
                self.val = nval
                self.board.append(state)

        if stats:
            self.get_stats(hist)

class AutoPlayer(object):
    """docstring for auto_player."""
    def __init__(self, symb=2, greedy=False, epsilon=0.05, step_size=0.1):
        self.symbol = symb
        self.greedy = greedy
        self.epsilon = epsilon
        self.step_size = step_size

    def setStepSize(self, step_size):
        self.step_size = step_size

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setGreedy(self, greedy):
        self.greedy = greedy

    def update_vals(self,board,val):
        for k in reversed(range(len(board)-1)):
            err = val[board[k+1]] - val[board[k]]
            val[board[k]] += self.step_size*err
        return val

    def move(self, board, val):
        possible_states = []
        for ind,state in enumerate(board[-1]):
            if state == 0:
                new_state = []
                for j in range(len(board[-1])):
                    if j == ind:
                        new_state.append(self.symbol)
                    else:
                        new_state.append(board[-1][j])
                possible_states.append(new_state)

        if random.random() < self.epsilon and not self.greedy:
            next_state = random.choice(possible_states)
        else:
            probs = [val[tuple(state)] for state in possible_states]
            next_states = [possible_states[i] for i,x in enumerate(probs) if x == max(probs)]
            next_state = random.choice(next_states)

            val = self.update_vals(board, val)

        return tuple(next_state),val

class HumanPlayer(object):
    """docstring for HumanPlayer."""
    def __init__(self, symb=1):
        self.symbol = symb

    def move(self, board, val):
        move = int(input("Enter position(0-8): "))
        valid = False
        while not valid:
            if 0 <= move <= 8:
                if board[-1][move] == 0:
                    new_state = list(board[-1])
                    new_state[move] = self.symbol
                    #board.append(tuple(new_state))
                    valid = True
                else:
                    move = int(input("Enter position(0-8): "))
            else:
                move = int(input("Enter position(0-8): "))
        return tuple(new_state),val
