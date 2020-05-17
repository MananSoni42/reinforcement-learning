from classes import Env, HumanSnake, AISnake, Game
import json
import numpy as np

N = 3
snake = AISnake(N, 0.9, weights=f'weights/{N}x{N}-2-weights.json')
game = Game(snake,N)
game.play(1,print_env=True, print_score=True)
