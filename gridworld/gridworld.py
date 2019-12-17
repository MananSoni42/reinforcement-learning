import numpy as np
from pprint import pprint
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import animation

GRID_COLS = 5
GRID_ROWS = 5
val_init = 0
itr = 100
gamma = 0.9

actions = {
    'L': (-1,0),
    'R': (1,0),
    'U': (0,-1),
    'D': (0,1),
}
# create vanilla grid
grid = dict()
for i in range(GRID_ROWS):
    for j in range(GRID_COLS):
        acts = dict()
        for a in actions:
            if 0 <= j+actions[a][0] < 5 and 0 <= i+actions[a][1] < 5:
                acts[a] = [0, GRID_COLS*(i+actions[a][1]) + j+actions[a][0]]
            else:
                acts[a] = [-1, GRID_COLS*i + j]
        grid[GRID_COLS*i + j] = acts

# special changes
grid[1]['L'] = [10,21]
grid[1]['R'] = [10,21]
grid[1]['U'] = [10,21]
grid[1]['D'] = [10,21]

grid[3]['L'] = [5,13]
grid[3]['R'] = [5,13]
grid[3]['U'] = [5,13]
grid[3]['D'] = [5,13]

pprint(grid)

# Define value function
val = val_init*np.ones(GRID_ROWS*GRID_COLS)
print(val.shape)

# 1. - Iterative scheme
for i in range(itr):
    for s in range(GRID_ROWS*GRID_COLS):
        state = grid[s]
        v = val[s]
        sum = 0
        for act in state:
            sum += 0.25*(state[act][0]+gamma*val[state[act][1]])
        val[s] = sum

for i in range(0,GRID_ROWS*GRID_COLS,5):
    print(val[i:i+5])
