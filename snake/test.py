from classes import Env, HumanSnake, AISnake, Game
import json
import numpy as np
np.random.seed()

N = 3
mem = 3
#snake = HumanSnake()
snake = AISnake(N=N, mem=mem, alpha=0.9, weights=f'final_weights/{N}x{N}-{mem}.json')
game = Game(snake,N)
game.play(1,print_env=True, print_score=True)
