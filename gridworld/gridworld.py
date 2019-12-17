import numpy as np
from pprint import pprint
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import animation
import time
import random

GRID_COLS = 5
GRID_ROWS = 5
val_init = 0
itr = 500
gamma = 0.9
starting_pt = 17  # 0-24

def next_step(val,s,a):
    possible_states = []
    for act in grid[s]:
        possible_states.append((grid[s][act][1],val[grid[s][act][1]]))
    possible_states = np.array(possible_states)
    try:
        ind = random.choice(np.argwhere(possible_states[:,1] == np.argmax(possible_states[:,1])))[0]
    except:
        ind = np.argmax(possible_states[:,1])
    nxt_st = int(possible_states[ind,0])
    new_a = a*0.5
    new_a[int(nxt_st/GRID_COLS),nxt_st%GRID_COLS] = 1
    return nxt_st,new_a

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

#pprint(grid)

# Define value function
val = val_init*np.ones(GRID_ROWS*GRID_COLS)

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

# visualize solution
current_state = starting_pt
data = np.zeros((GRID_ROWS,GRID_COLS))
data[int(starting_pt/GRID_COLS),starting_pt%GRID_COLS] = 1

# create discrete colormap
col_map = plt.get_cmap('Blues')
fig, ax = plt.subplots()
im = plt.imshow(data, cmap=col_map)

def init():
    global data
    im.set_data(data)
    return [im]

# animation function.  This is called sequentially
def animate(i):
    global current_state,data,val,col_map
    current_state, data = next_step(val,current_state,data)
    im.set_array(data)
    time.sleep(1)
    return [im]

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=1, interval=20, blit=True)
plt.show()
