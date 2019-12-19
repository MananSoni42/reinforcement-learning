import numpy as np
import random
import matplotlib.pyplot as plt
from pprint import pprint
import random
from tqdm import tqdm

# H --> 0
# T --> 1

MAX_AMT  = 99
itr = 2000
gamma = 0.9
prob_head = 0.4

# states are 0 to MAX_AMT
val = np.zeros(MAX_AMT+1)
#val[MAX_AMT] = 1
rew = np.zeros(MAX_AMT+1)
rew[MAX_AMT] = 1

plt.subplot(221)
plt.title('Initial value function')
plt.plot(val)

# 1. Value iteration - get value function
for i in tqdm(range(itr)):
    for j in range(val.shape[0]):
        acts = []
        act_range = list(range(min(j, MAX_AMT - j) + 1))
        for a in act_range:
            acts.append( prob_head*(rew[j+a] + gamma*val[j+a]) + (1-prob_head)*(rew[j-a] + gamma*val[j-a]) )
            #acts.append( prob_head*val[j+a] + (1-prob_head)*(val[j-a]) )
        val[j] = np.max(acts)
val = np.round(val,5)
plt.subplot(222)
plt.title(f'Final value function ({itr} iterations)')
plt.plot(val)

# 2. Get optimal policy
pol = np.zeros(MAX_AMT+1)
for i in range(1,val.shape[0]-1):
    acts = []
    act_range = np.arange(min(i, MAX_AMT - i) + 1)
    for a in act_range:
        acts.append( prob_head*(rew[i+a] + gamma*val[i+a]) + (1-prob_head)*(rew[i-a] + gamma*val[i-a]) )
        #acts.append( prob_head*val[i+a] + (1-prob_head)*(val[i-a]) )

    acts = np.round(acts[1:],5)
    try:
        ind = random.choice(np.argwhere(acts==np.max(acts)))
    except:
        ind = np.argmax(acts)
    pol[i] = act_range[ind+1]

print(f'Gambler\' problem: p_h = {prob_head}')
print('Reward:')
print(rew)
print('Value:')
print(val)
print('Policy:')
print(pol)

plt.subplot(223)
plt.title('Final policy (scatterplot)')
plt.scatter(range(len(pol)),pol,s=5)
plt.subplot(224)
plt.title('Final policy (line chart)')
plt.plot(pol)
plt.show()
