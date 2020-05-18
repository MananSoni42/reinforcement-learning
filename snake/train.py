from classes import Env, HumanSnake, AISnake, Game
import numpy as np
import json
import sys

N = int(sys.argv[1])
mem = int(sys.argv[2]) # 0 1 2 3 supported
num = int(sys.argv[3])
num_iters_play = 1000
alphas = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1]
eps = 0.05

best_q =dict()
best_mean = 0
best_sc = dict()
best_alpha = 0

#snake = HumanSnake()
for alpha in alphas: # broad sweep
    alpha = round(alpha,3)
    snake = AISnake(N=N,mem=mem, alpha=alpha)
    game = Game(snake, N)
    print(f'\n{N},{mem} a: ',alpha)
    game.train(num=int(num), print_every=int(num/5))
    sc = game.play(num=num_iters_play, print_score=False)
    mean = np.sum([k*v for k,v in sc.items()])/num_iters_play
    print(f'Mean({alpha}): ', mean)
    if best_mean < mean:
        best_alpha = alpha
        best_mean = mean
        best_sc = sc
        best_q = snake.Q

with open(f'final_weights/{N}x{N}-{mem}.json','w') as f:
    print(f'{N},{mem} Best distr: ',best_sc)
    print(f'Mean({best_alpha}): ', best_mean)
    json.dump({
                'N': N,
                'distribution': best_sc,
                'mean': best_mean,
                'weights': {k:[v[0].tolist(),v[1]] for k,v in best_q.items()},
                },
                f,
                indent=2,
            )
