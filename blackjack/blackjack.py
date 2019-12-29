import numpy as np
import random
from pprint import pprint
from tqdm import tqdm
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# 0 -> STICK
# 1 -> HIT
ACTIONS = [0,1]

# keys are states
# state: (player's sum, dealer's open card, usable ace)
val = dict()

player_policy  = lambda state: 1 if state[0] < 20 else 0
dealer_policy  = lambda sum: 1 if sum < 17 else 0

def player_policy_target(state):
    action = 0
    if state['sum'] in [20,21]:
        action = 1
    return action

def player_policy_behaviour(state):
    return np.random.binomial(1,0.5) # choose actions randomly (50% probability each)

def get_card():
    card = np.random.randint(1, 14)
    return card

card_value = lambda card: 11 if card==1 else min(card,10)


def generate_episode(target_policy, initial_state=None, initial_action=None):
    finish = False
    dealer_card1 = -1
    dealer_card2 = -1
    dealer_sum = 0
    dealer_usable_ace = False

    player_usable_ace = False
    player_sum = 0

    if initial_state is None:
        # initialize cards of dealer, suppose dealer will show the first card he gets
        dealer_card1 = get_card()
        dealer_card2 = get_card()

        # initialize cards of player
        while player_sum < 12:
            card = get_card()
            player_sum += card_value(card)

            if player_sum > 21:
                player_sum -= 10 # replace Ace (11) by Ace(1)
            elif card == 1:
                player_usable_ace = True

    else:
        player_sum, player_usable_ace, dealer_card1 = initial_state
        dealer_card2 = get_card()

    assert dealer_sum <= 21
    assert player_sum <= 21

    # game state
    state = (player_sum,player_usable_ace,dealer_card1)

    # initialize dealer's state
    dealer_sum = card_value(dealer_card1) + card_value(dealer_card2)
    dealer_usable_ace = 1 in (dealer_card1, dealer_card2)
    if dealer_sum > 21:
        assert dealer_sum == 22
        # use one Ace as 1 rather than 11
        dealer_sum -= 10

    # play 1 game until it's end
    history = [state]
    reward = 0
    stop = False

    ace_count = int(state[1])
    if initial_action is not None:
        action = initial_action
        initial_action = None
    else:
        # get action based on current sum
        action = target_policy(state)

    # player's chance
    while action == 1:
        if action == 0:
            chance = 1
            break
        card = get_card()
        if card == 1:
            ace_count += 1
        player_sum += card_value(card)

        if player_sum == 21: # player wins or draws
            if dealer_sum == 21:
                reward = 0
                finish = True
                break
            else:
                reward = 1
                finish = True
                break

        elif player_sum > 21: # player loses or converts ace(11) to ace(1)
            if ace_count != 0:
                player_sum -= 10
                if ace_count == 1:
                    player_usable_ace = False
            else:
                reward = -1
                finish = True
                break
        state = (player_sum, player_usable_ace, dealer_card1)
        history.append(state)

    # dealer's chance
    dealer_action = dealer_policy(dealer_sum)
    dealer_ace_count = int(dealer_usable_ace)
    while dealer_action == 1 and not finish:
        if dealer_action == 0:
            break
        card = get_card()
        if card == 1:
            dealer_ace_count += 1

        dealer_sum += card_value(card)

        if dealer_sum == 21: # dealer wins or draws
            if player_sum == 21:
                reward = 0
                break
            else:
                reward = -1
                break

        if dealer_sum > 21: # dealer loses or converts ace(11) to ace(1)
            if dealer_ace_count != 0:
                dealer_sum -= 10
                if dealer_ace_count == 1:
                    dealer_usable_ace = False
            else:
                reward = 1
                break

    if player_sum < 21 and dealer_sum < 21:
        if player_sum == dealer_sum:
            reward = 0
        else:
            reward = -1 + 2*int(player_sum > dealer_sum)
    return history, reward

# Generate one episode as trial
# pprint(generate_episode(player_policy))

def monte_carlo_on_policy_eval(episodes):
    print('start')
    states_usable_ace = np.zeros((10, 10))
    states_usable_ace_count = np.ones((10, 10))
    states_no_usable_ace = np.zeros((10, 10))
    states_no_usable_ace_count = np.ones((10, 10))

    for _ in tqdm(range(episodes)):
        hist, reward = generate_episode(player_policy)
        for (player_sum,usable_ace,dealer_card) in hist:
                dealer_card = card_value(dealer_card) # get value of dealer's card
                dealer_card -= 1 # dealer's card value is in the range 1-11
                if dealer_card == 10: # rename ace to 1
                    dealer_card = 0
                player_sum = min(player_sum,21) - 12 # player's sum is in the range 12-*
                if usable_ace:
                    states_usable_ace[player_sum,dealer_card] += reward
                    states_usable_ace_count[player_sum,dealer_card] += 1
                else:
                    states_no_usable_ace[player_sum,dealer_card] += reward
                    states_no_usable_ace_count[player_sum,dealer_card] += 1
    plt.figure(1)
    ax = plt.axes(projection='3d')
    x,y = np.meshgrid(np.arange(12,21+1), np.arange(1,10+1))
    #ax.plot_wireframe(x, y, states_usable_ace/states_usable_ace_count)
    ax.plot_surface(x, y, states_usable_ace/states_usable_ace_count)
    ax.set_xlabel('Player sum')
    ax.set_ylabel('Dealer\'s card')
    ax.set_zlabel('Value');
    ax.set_title('Usable Ace')

    plt.figure(2)
    ax = plt.axes(projection='3d')
    x,y = np.meshgrid(np.arange(12,21+1), np.arange(1,10+1))
    #ax.plot_wireframe(x, y, states_usable_ace/states_usable_ace_count)
    ax.plot_surface(x, y, states_no_usable_ace/states_no_usable_ace_count)
    ax.set_xlabel('Player sum')
    ax.set_ylabel('Dealer\'s card')
    ax.set_zlabel('Value');
    ax.set_title('No usable Ace')
    plt.show()

monte_carlo_on_policy_eval(100000)
