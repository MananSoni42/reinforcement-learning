import numpy as np
from tqdm import tqdm
import json

object = {
    'empty': 0,
    'snake-body': 1,
    'snake-head': 2,
    'food': 3
}

action = {
    'left': (0,-1),
    'right': (0,1),
    'up': (-1,0),
    'down': (1,0),
}

action_enc = {
    'left': 0,
    'right': 1,
    'up': 2,
    'down': 3,
}

reward = {
    'food': 5,
    'bump': -1,
    'time': -0.1
}


def str_to_list(s,spl=', '):
    print(s)
    s = s.replace('(','').replace(')','').replace('[','').replace(']','').split(spl)
    l = tuple([int(v) for v in s])
    print(l)
    return l

class Env:
    """grid for """
    def __init__(self, N, snake):
        self.N = N
        self.end = False
        self.grid = np.zeros((self.N,self.N))
        self.snake = snake
        self.food = False
        self.score = 0

    def reset(self):
        self.end = False
        self.grid = np.zeros((self.N,self.N))
        self.food = False
        self.score = 0

    def __str__(self):
        s = []
        for i in range(self.N):
            for j in range(self.N):
                if self.grid[i][j] == object['snake-head']:
                    s.append('0 ')
                elif self.grid[i][j] == object['snake-body']:
                    s.append('o ')
                elif self.grid[i][j] == object['food']:
                    s.append('* ')
                else :
                    s.append('- ')
            s.append('\n')
        return ''.join(s)

    def create_food(self):
        possibilities = np.where(self.grid == 0)
        try:
            ind = np.random.randint(possibilities[0].shape)[0]
        except ValueError:
            self.end = True
            return
        self.grid[possibilities[0][ind],possibilities[1][ind]] = object['food']
        self.food = True

    def get_state(self):
        if len(self.snake.last) < 2:
            while (len(self.snake.last) != 3):
                self.snake.last.insert(0,-1)
        lasts = self.snake.last[-3:]
        x1,y1 = self.snake.pos[-1]
        if self.end:
            x2,y2 = 0,0
        else:
            x2,y2 = np.where(self.grid==object['food'])
            x2 = x2[0]
            y2 = y2[0]

        return str((x1,y1,x2,y2,lasts[-1],lasts[-2]))

    def next(self,a,print_score=False):
        self.snake.last.append(action_enc[a])
        r = reward['time']
        self.grid[self.snake.pos[-1]] = object['snake-body']

        x,y = self.snake.pos[-1]
        x += action[a][0]
        y += action[a][1]
        if not (0 <= x < self.N and 0 <= y < self.N):
            self.end = True
            r += reward['bump']
        elif self.grid[x,y] == object['snake-body']:
            self.end = True
            r += reward['bump']
            self.snake.pos.append((x,y))
            self.grid[x,y] = object['snake-head']
        elif self.grid[x,y] == object['food']:
            r += reward['food']
            self.food = False
            self.score += 1
            self.snake.pos.append((x,y))
            self.grid[x,y] = object['snake-head']
        else:
            self.grid[self.snake.pos[0]] = 0
            self.snake.pos.pop(0)
            self.snake.pos.append((x,y))
            self.grid[x,y] = object['snake-head']

        if not self.food:
            self.create_food()

        if print_score:
            print("score: ",self.score, '\n')

        return r, self.get_state(), self.score


class HumanSnake:
    """class for snake object can move"""

    def __init__(self, pos=(0,0)):
        self.pos = [pos] # entire snake -> head last

    def reset(self, pos):
        self.pos = [pos]

    def move(self, reward, state):
        a = input('Enter move: ').lower()
        while a not in ['w','a','s','d']:
            a = input('Enter move: ').lower()

        if a == 'w':
            return 'up'
        elif a == 'a':
            return 'left'
        elif a == 's':
            return 'down'
        elif a == 'd':
            return 'right'

class AISnake:
    """class for snake object can move"""

    def __init__(self, N, alpha=0.1, pos=(0,0), weights=None):
        self.pos = [pos] # entire snake -> head last
        self.alpha = alpha
        self.state = -1
        self.action = -1
        self.Q = dict()
        self.last = [] # last 3
        if weights:
            with open(weights) as f:
                self.Q = json.load(f)['weights']
        else:
            print('Initializing...')
            for x1 in tqdm(range(N)):
                for y1 in range(N):
                    for x2 in range(N):
                        for y2 in range(N):
                            for j1 in range(-1,3+1):
                                for j2 in range(-1,3+1):
                                    #for j3 in range(-1,3+1):
                                    self.Q[str((x1,y1,x2,y2,j1,j2))] = np.array([0,0,0,0]) # U,D,L,R


    def reset(self, pos):
        self.last = []
        self.pos = [pos] # entire snake -> head last
        self.state = -1
        self.action = -1

    def move(self, reward, state): # TD
        if self.state == -1:
            act = np.random.randint(4)
        else:
            #print(state)
            #print(self.Q[state])
            max_val = np.max(self.Q[state])
            act = np.random.choice(np.where(self.Q[state]==max_val)[0])
            self.Q[self.state][self.action] += self.alpha*(reward + max_val - self.Q[self.state][self.action]) # TD
            #self.Q[self.state][self.action] += self.alpha*(reward + self.Q[self.state][act] - self.Q[self.state][self.action]) # SARSA

        self.state = state
        self.action = act

        if act == 0:
            return 'up'
        if act == 1:
            return 'down'
        if act == 2:
            return 'left'
        if act == 3:
            return 'right'

class Game:
    """docstring for Game."""

    def __init__(self, s, N, print_every=100):
        self.snake = s
        self.N = N
        self.snake.pos[0] = (int(N/2),int(N/2))
        self.env = Env(N, s)
        self.env.grid[self.snake.pos[-1]] = object['snake-head']
        self.env.create_food()

    def train(self, num, print_every=None, decay=0.95, decay_every=None):
        if not decay_every:
            decay_every = int(num/15)
        if not print_every:
            print_every = int(num/20)

        r = 0
        s = self.env.get_state()
        flag1 = True
        flag2 = True
        count = 1
        scorenum = 0
        scoredenom = 0
        sc = 0
        while (count<=num):
            if flag1 and count%print_every==0:
                score = scorenum/scoredenom
                print('\t it:', count, '/', num, ' Avg: ', round(score,2), ' a: ', self.snake.alpha)
                #scorenum = 0
                #scoredenom = 0
                flag1 = False

            if flag2 and count%decay_every == 0:
                self.snake.alpha *= decay
                flag2 = False

            if self.env.end:
                scorenum += sc
                scoredenom += 1
                count += 1
                flag1 = True
                flag2 = True
                self.env.reset()
                self.snake.reset((int(self.N/2),int(self.N/2)))
                self.env.grid[self.snake.pos[0]] = object['snake-head']
                self.env.create_food()
                s = self.env.get_state()

            #print(self.env)
            a = self.snake.move(r,s)
            r,s,sc = self.env.next(a)

    def play(self, num, print_score=False, print_env=False):
        sc = 0
        mx = 0
        scr = dict()
        for i in range(num):
            self.env.reset()
            self.snake.reset((int(self.N/2),int(self.N/2)))
            self.env.grid[self.snake.pos[0]] = object['snake-head']
            self.env.create_food()
            r = 0
            s = self.env.get_state()
            sc = 0
            while (not self.env.end):
                if print_env:
                    print(self.env)
                a = self.snake.move(r,s)
                r,s,sc = self.env.next(a, print_score=print_score)
            if sc in scr:
                scr[sc] += 1
            else:
                scr[sc] = 1
        return scr
