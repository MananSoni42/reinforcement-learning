import numpy as np
from tqdm import tqdm
import json
np.random.seed(42)

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
    'up': 0,
    'down': 1,
    'left': 2,
    'right': 3,
}

reward = {
    'food': 10,
    'bump': -3,
    'time': 0
}

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
        if len(self.snake.last) < self.snake.mem:
            while (len(self.snake.last) != self.snake.mem):
                self.snake.last.insert(0,-1)
        lasts = self.snake.last[-3:]
        x1,y1 = self.snake.pos[-1]
        if self.end:
            x2,y2 = 0,0
        else:
            x2,y2 = np.where(self.grid==object['food'])
            x2 = x2[0]
            y2 = y2[0]

        if self.snake.mem == 0:
            return str((x1,y1,x2,y2))
        elif self.snake.mem == 1:
            return str((x1,y1,x2,y2,lasts[-1]))
        elif self.snake.mem == 2:
            return str((x1,y1,x2,y2,lasts[-1],lasts[-2]))
        elif self.snake.mem == 3:
            return str((x1,y1,x2,y2,lasts[-1],lasts[-2],lasts[-3]))

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
        self.last = [] # last actions

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

    def __init__(self, N, mem=2, alpha=0.1, pos=(0,0), weights=None, init_val=1):
        self.pos = [pos] # entire snake -> head last
        self.alpha = alpha
        self.mem = mem
        self.state = -1
        self.action = -1
        self.Q = dict()
        self.last = [] # last actions
        if weights:
            with open(weights) as f:
                self.Q = json.load(f)['weights']
        else:
            #print('Initializing...')
            for x1 in range(N):
                for y1 in range(N):
                    for x2 in range(N):
                        for y2 in range(N):
                            for j in range(pow(5,mem)):
                                arr = np.array([init_val,init_val,init_val,init_val], dtype=np.float32)
                                num = 0
                                if mem == 0:
                                    self.Q[str((x1,y1,x2,y2))] = [arr,num] # U,D,L,R
                                elif mem == 1:
                                    self.Q[str((x1,y1,x2,y2,j-1))] = [arr,num] # U,D,L,R
                                elif mem == 2:
                                    self.Q[str((x1,y1,x2,y2,int(j/5)%5-1,(j%5)-1))] = [arr,num] # U,D,L,R
                                elif mem == 3:
                                    self.Q[str((x1,y1,x2,y2,int(j/25)%5-1,int(j/5)%5-1,(j%5)-1))] = [arr,num] # U,D,L,R


    def reset(self, pos):
        self.last = []
        self.pos = [pos] # entire snake -> head last
        self.state = -1
        self.action = -1

    def move(self, reward, state,test=False): # TD
        if self.state == -1:
            act = np.random.randint(4)
        else:
            self.Q[state][1] += 1
            #max_val = np.max(self.Q[state][0])
            if test:
                act = np.random.choice(np.where(self.Q[state][0]==np.max(self.Q[state][0]))[0])
            else:
                probs = (self.Q[state][0]+np.abs(np.min(self.Q[state][0])))/np.sum(self.Q[state][0]+np.abs(np.min(self.Q[state][0])))
                #probs = np.exp(self.Q[state][0])/np.sum(np.exp(self.Q[state][0]))
                act = np.random.choice(np.array([0,1,2,3]), p=probs)

            if not test:
                self.Q[self.state][0][self.action] += self.alpha*np.exp(-self.Q[self.state][1]/100)*(reward + self.Q[state][0][act] - self.Q[self.state][0][self.action]) # TD
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

    def train(self, num, print_every=None, decay=1, decay_every=None):
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
        l = 0
        l_temp = 0

        while (count<=num):
            if flag1 and count%print_every==0:
                score = scorenum/scoredenom
                #print(f'\t it: {int(100*count/num)}% | score: {round(score,2)} | len: {round(l/scoredenom,2)} | a: {round(self.snake.alpha,3)}')
                print(f'\t it: {int(100*count/num)}% | score: {round(score,2)} | len: {round(l/scoredenom,2)}')
                #scorenum = 0
                #scoredenom = 0
                flag1 = False

            if flag2 and count%decay_every == 0:
                self.snake.alpha *= decay
                flag2 = False

            if self.env.end:
                l += l_temp
                l_temp = 0
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
            l_temp += 1
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
                a = self.snake.move(r,s,test=True)
                #print(s,self.snake.Q[s],a)
                r,s,sc = self.env.next(a, print_score=print_score)
            if sc in scr:
                scr[sc] += 1
            else:
                scr[sc] = 1
        return scr
