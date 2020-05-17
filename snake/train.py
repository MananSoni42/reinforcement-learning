from classes import Env, HumanSnake, AISnake, Game
import numpy as np
import json
import sys

class ListEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj,list):
            return obj
        return json.JSONEncoder.default(self, obj)

N = int(sys.argv[1])
num = 250000
num_iters_play = 1000
alphas = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3]
eps = 0.05

best_q =dict()
best_mean = 0
best_sc = dict()
best_alpha = 0

#snake = HumanSnake()
for alpha in alphas: # broad sweep
    snake = AISnake(N,alpha)
    game = Game(snake, N)
    print('\na: ',alpha)
    game.train(num=int(num/5), print_every=int(num/50))
    sc = game.play(num=num_iters_play, print_score=False)
    mean = np.sum([k*v for k,v in sc.items()])/num_iters_play
    print(f'Mean({alpha}): ', mean)
    if best_mean < mean:
        best_alpha = alpha
        best_mean = mean
        best_sc = sc
        best_q = snake.Q

for alpha in np.arange(best_alpha-eps,best_alpha+2*eps,eps): # fine sweep
    snake = AISnake(N,alpha)
    game = Game(snake, N)
    print('\na: ',alpha)
    game.train(num=num, print_every=int(num/5))
    sc = game.play(num=num_iters_play, print_score=False)
    mean = np.sum([k*v for k,v in sc.items()])/num_iters_play
    print(f'Mean({alpha}): ', mean)
    if best_mean < mean:
        best_mean = mean
        best_sc = sc
        best_q = snake.Q

with open(f'weights/{N}x{N}-2-weights.json','w') as f:
    print('Best distr: ',best_sc)
    print(f'Mean({best_alpha}): ', best_mean)
    json.dump({
                'N': N,
                'distribution': best_sc,
                'mean': best_mean,
                'weights': {k:v for k,v in best_q.items()},
            },
            f,
            indent=2,
            cls=ListEncoder)
