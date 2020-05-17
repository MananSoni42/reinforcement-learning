import numpy as np
from tqdm import tqdm

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

reward = {
    'food': 5,
    'bump': -1,
    'time': -0.1
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
        num = 0
        if self.end:
            x1,y1 = self.snake.pos[-1]
            x2,y2 = 0,0
            return (x1,y1,x2,y2,num)

        x1,y1 = self.snake.pos[-1]
        x2,y2 = np.where(self.grid==object['food'])
        x2 = x2[0]
        y2 = y2[0]

        for i in range(-1,1+1):
            for j in range(-1,1+1):
                if (i,j) != (0,0):
                    try:
                        val = self.grid[self.snake.pos[0][0]+i, self.snake.pos[0][1]+j]
                        val = int(val==1 or val==2)
                    except IndexError:
                        val = 0
                    ind = (i+1)*3 + (j+1)
                    if ind>4:
                        ind -= 1
                    num += pow(2,7-ind)*val

        return (x1,y1,x2,y2,num)

    def next(self,a,print_score=False):
        r = reward['time']
        self.grid[self.snake.pos[-1]] = object['snake-body']

        x,y = self.snake.pos[-1]
        x += action[a][0]
        y += action[a][1]
        if not (0 <= x < self.N and 0 <= y < self.N):
            self.end = True
            r = reward['bump']
        elif self.grid[x,y] == object['snake-body']:
            self.end = True
            r = reward['bump']
            self.snake.pos.append((x,y))
            self.grid[x,y] = object['snake-head']
        elif self.grid[x,y] == object['food']:
            r = reward['food']
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

    def __init__(self, N, pos=(0,0), alpha=0.1):
        self.pos = [pos] # entire snake -> head last
        self.alpha = alpha
        self.state = -1
        self.action = -1
        self.Q = dict()
        print('Initializing...')
        for x1 in tqdm(range(N)):
            for y1 in range(N):
                for x2 in range(N):
                    for y2 in range(N):
                        for j in range(256):
                            self.Q[x1,y1,x2,y2,j] = np.array([0,0,0,0]) # U,D,L,R

    def reset(self, pos):
        self.pos = [pos] # entire snake -> head last
        self.state = -1
        self.action = -1

    def move(self, reward, state): # TD
        if self.state == -1:
            act = np.random.randint(4)
        else:
            max_val = np.max(self.Q[state])
            act = np.random.choice(np.where(self.Q[state]==max_val)[0])
            #self.Q[self.state][self.action] += self.alpha*(reward + max_val - self.Q[self.state][self.action]) # TD
            self.Q[self.state][self.action] += self.alpha*(reward + self.Q[self.state][act] - self.Q[self.state][self.action]) # SARSA

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

    def __init__(self, s, N, num, print_every=100):
        self.snake = s
        self.print_every = print_every
        self.N = N
        self.snake.pos[0] = (int(N/2),int(N/2))
        self.env = Env(N, s)
        self.env.grid[self.snake.pos[-1]] = object['snake-head']
        self.env.create_food()
        self.num = num

    def train(self):
        r = 0
        s = self.env.get_state()
        flag = True
        count = 1
        scorenum = 0
        scoredenom = 0
        sc = 0
        while (count<=self.num):
            if (flag and count%self.print_every==0):
                self.snake.alpha = self.snake.alpha*0.95
                score = scorenum/scoredenom
                print('iteration ', count, '/', self.num, ' Average score: ', round(score,2))
                scorenum = 0
                scoredenom = 0
                flag = False

            if self.env.end:
                scorenum += sc
                scoredenom += 1
                count += 1
                flag = True
                self.env.reset()
                self.snake.reset((int(self.N/2),int(self.N/2)))
                self.env.grid[self.snake.pos[0]] = object['snake-head']
                self.env.create_food()
                s = self.env.get_state()

            #print(self.env)
            a = self.snake.move(r,s)
            r,s,sc = self.env.next(a)

    def play(self):
        self.env.reset()
        self.snake.reset((int(self.N/2),int(self.N/2)))
        self.env.grid[self.snake.pos[0]] = object['snake-head']
        self.env.create_food()
        r = 0
        s = self.env.get_state()

        while (not self.env.end):
            print(self.env)
            a = self.snake.move(r,s)
            r,s,_ = self.env.next(a, print_score=True)
