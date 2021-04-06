import numpy as np
from copy import deepcopy
from functools import reduce
from operator import add
import os

HEALTH_RANGE = 5
ARROWS_RANGE = 4
MATERIAL_RANGE = 3
POSITION_RANGE = 5
MOOD_RANGE = 2

HEALTH_VALUES = tuple(range(HEALTH_RANGE))
ARROWS_VALUES = tuple(range(ARROWS_RANGE))
MATERIAL_VALUES = tuple(range(MATERIAL_RANGE))
POSITION_VALUES = tuple(range(POSITION_RANGE))
MOOD_VALUES = tuple(range(MOOD_RANGE))

HEALTH_FACTOR = 25 # 0, 25, 50, 75, 100
ARROWS_FACTOR = 1 # 0, 1, 2, 3
MATERIAL_FACTOR = 1 # 0, 1, 2
POSITION_FACTOR = 1 # (0, north), (1, east), (2, south), (3, west), (4, center)
MOOD_FACTOR = 1 # 0 - dormant, 1 - ready

NUM_ACTIONS = 5 # (move, shoot, hit), (move, craft), (move, gather), (move, shoot, hit), (move, shoot)
ACTION_MOVE = 0
ACTION_SHOOT = 4
ACTION_HIT = 1
ACTION_CRAFT = 3
ACTION_GATHER = 2

TEAM = 21
Y = 0.5
PRIZE = 50
COST = -20

GAMMA = 0.999
DELTA = 0.001

REWARD = np.zeros((POSITION_RANGE, HEALTH_RANGE, ARROWS_RANGE, MATERIAL_RANGE, MOOD_RANGE))
REWARD[:, 0, :, :, :] = PRIZE
# print(REWARD)

class State:
    def __init__(self, position, enemy_health, num_arrows, materials, mood):
        if (enemy_health not in HEALTH_VALUES) or (num_arrows not in ARROWS_VALUES) or (materials not in MATERIAL_VALUES):
            raise ValueError

        self.position = position
        self.health = enemy_health
        self.arrows = num_arrows
        self.materials = materials
        self.mood = mood

    def show(self):
        return (self.position, self.health, self.arrows, self.materials, self.mood)

    def __str__(self):
        return f'({self.position}, {self.health},{self.arrows},{self.materials}, {self.mood})'

def action(action_type, state, costs):
    # returns cost, array of tuple of (probability, state)

    state = State(*state)

    if action_type == ACTION_SHOOT:
        if state.arrows == 0:
            return None, None

        new_arrows = state.arrows - 1

        choices = []
        if state.position == 1:
            if state.mood == 0:
                choices.append(
                    (0.18, State(state.position, max(HEALTH_VALUES[0], state.health-1), new_arrows, state.materials, 1)))
                choices.append((0.02, State(state.position, state.health, new_arrows, state.materials, 1)))
                choices.append(
                    (0.72, State(state.position, max(HEALTH_VALUES[0], state.health-1), new_arrows, state.materials, 0)))
                choices.append((0.08, State(state.position, state.health, new_arrows, state.materials, 0)))
            elif state.mood == 1:
                choices.append((0.5, State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0)))
                REWARD[State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0).show()] = -40
                choices.append((0.45, State(state.position, max(HEALTH_VALUES[0], state.health-1), new_arrows, state.materials, 1)))
                choices.append((0.05, State(state.position, max(HEALTH_VALUES[0], state.health), new_arrows, state.materials, 1)))

        elif state.position == 3:
            if state.mood == 0:
                choices.append(
                    (0.05, State(state.position, max(HEALTH_VALUES[0], state.health-1), new_arrows, state.materials, 1)))
                choices.append((0.15, State(state.position, state.health, new_arrows, state.materials, 1)))
                choices.append(
                    (0.2, State(state.position, max(HEALTH_VALUES[0], state.health-1), new_arrows, state.materials, 0)))
                choices.append((0.6, State(state.position, state.health, new_arrows, state.materials, 0)))
            elif state.mood == 1:
                choices.append((0.125, State(state.position, max(HEALTH_VALUES[0], state.health-1), new_arrows, state.materials, 0)))
                choices.append((0.375, State(state.position, max(HEALTH_VALUES[0], state.health), new_arrows, state.materials, 0)))
                choices.append((0.125, State(state.position, max(HEALTH_VALUES[0], state.health-1), new_arrows, state.materials, 1)))
                choices.append((0.375, State(state.position, max(HEALTH_VALUES[0], state.health), new_arrows, state.materials, 1)))

        elif state.position == 4:
            if state.mood == 0:
                choices.append(
                    (0.1, State(state.position, max(HEALTH_VALUES[0], state.health-1), new_arrows, state.materials, 1)))
                choices.append((0.1, State(state.position, state.health, new_arrows, state.materials, 1)))
                choices.append(
                    (0.4, State(state.position, max(HEALTH_VALUES[0], state.health-1), new_arrows, state.materials, 0)))
                choices.append((0.4, State(state.position, state.health, new_arrows, state.materials, 0)))
            elif state.mood == 1:
                choices.append((0.5, State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0)))
                REWARD[State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0).show()] = -40
                choices.append((0.25, State(state.position, max(HEALTH_VALUES[0], state.health-1), 0, state.materials, 1)))
                choices.append((0.25, State(state.position, max(HEALTH_VALUES[0], state.health), 0, state.materials, 1)))
        else:
            return None, None

        cost = 0
        for choice in choices:
            cost += choice[0] * (costs[ACTION_SHOOT] + REWARD[choice[1].show()])

        return cost, choices

    elif action_type == ACTION_HIT:
        choices = []

        if state.position == 1:
            if state.mood == 0:
                choices.append(
                    (0.04, State(state.position, max(HEALTH_VALUES[0], state.health-2), state.arrows, state.materials, 1)))
                choices.append((0.16, State(state.position, state.health, state.arrows, state.materials, 1)))
                choices.append(
                    (0.16, State(state.position, max(HEALTH_VALUES[0], state.health-2), state.arrows, state.materials, 0)))
                choices.append((0.64, State(state.position, state.health, state.arrows, state.materials, 0)))
            elif state.mood == 1:
                choices.append((0.5, State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0)))
                REWARD[State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0).show()] = -40
                choices.append((0.1, State(state.position, max(HEALTH_VALUES[0], state.health-2), state.arrows, state.materials, 1)))
                choices.append((0.4, State(state.position, state.health, state.arrows, state.materials, 1)))

        elif state.position == 4:
            if state.mood == 0:
                choices.append(
                    (0.02, State(state.position, max(HEALTH_VALUES[0], state.health-2), state.arrows, state.materials, 1)))
                choices.append((0.18, State(state.position, state.health, state.arrows, state.materials, 1)))
                choices.append(
                    (0.08, State(state.position, max(HEALTH_VALUES[0], state.health-2), state.arrows, state.materials, 0)))
                choices.append((0.72, State(state.position, state.health, state.arrows, state.materials, 0)))
            elif state.mood == 1:
                choices.append((0.5, State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0)))
                REWARD[State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0).show()] = -40
                choices.append(
                    (0.05, State(state.position, max(HEALTH_VALUES[0], state.health-2), state.arrows, state.materials, 1)))
                choices.append((0.45, State(state.position, state.health, state.arrows, state.materials, 1)))

        else:
            return None, None

        cost = 0
        for choice in choices:
            cost += choice[0] * (costs[ACTION_HIT] + REWARD[choice[1].show()])

        return cost, choices

    elif action_type == ACTION_CRAFT:
        if state.materials == 0:
            return None, None

        choices = []
        if state.position == 0 and state.materials > 0 and state.arrows < 3:
            if state.mood == 0:
                choices.append((0.1, State(state.position, state.health, min(
                    ARROWS_VALUES[-1], state.arrows+1), max(MATERIAL_VALUES[0], state.materials - 1), 1)))
                choices.append((0.07, State(state.position, state.health, min(
                    ARROWS_VALUES[-1], state.arrows+2), max(MATERIAL_VALUES[0], state.materials - 1), 1)))
                choices.append((0.03, State(state.position, state.health, min(
                    ARROWS_VALUES[-1], state.arrows+3), max(MATERIAL_VALUES[0], state.materials - 1), 1)))
                choices.append((0.4, State(state.position, state.health, min(
                    ARROWS_VALUES[-1], state.arrows+1), max(MATERIAL_VALUES[0], state.materials - 1), 0)))
                choices.append((0.28, State(state.position, state.health, min(
                    ARROWS_VALUES[-1], state.arrows+2), max(MATERIAL_VALUES[0], state.materials - 1), 0)))
                choices.append((0.12, State(state.position, state.health, min(
                    ARROWS_VALUES[-1], state.arrows+3), max(MATERIAL_VALUES[0], state.materials - 1), 0)))
            elif state.mood == 1:
                if state.position == 1 or state.position == 4:
                    choices.append((0.5, State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0)))
                    REWARD[State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0).show()] = -40
                    choices.append((0.25, State(state.position, state.health, min(
                        ARROWS_VALUES[-1], state.arrows+1), max(MATERIAL_VALUES[0], state.materials - 1), 1)))
                    choices.append((0.175, State(state.position, state.health, min(
                        ARROWS_VALUES[-1], state.arrows+2), max(MATERIAL_VALUES[0], state.materials - 1), 1)))
                    choices.append((0.075, State(state.position, state.health, min(
                        ARROWS_VALUES[-1], state.arrows+3), max(MATERIAL_VALUES[0], state.materials - 1), 1)))
                else:
                    choices.append((0.25, State(state.position, state.health, min(
                        ARROWS_VALUES[-1], state.arrows+1), max(MATERIAL_VALUES[0], state.materials - 1), 0)))
                    choices.append((0.175, State(state.position, state.health, min(
                        ARROWS_VALUES[-1], state.arrows+2), max(MATERIAL_VALUES[0], state.materials - 1), 0)))
                    choices.append((0.075, State(state.position, state.health, min(
                        ARROWS_VALUES[-1], state.arrows+3), max(MATERIAL_VALUES[0], state.materials - 1), 0)))
                    choices.append((0.25, State(state.position, state.health, min(
                        ARROWS_VALUES[-1], state.arrows+1), max(MATERIAL_VALUES[0], state.materials - 1), 1)))
                    choices.append((0.175, State(state.position, state.health, min(
                        ARROWS_VALUES[-1], state.arrows+2), max(MATERIAL_VALUES[0], state.materials - 1), 1)))
                    choices.append((0.075, State(state.position, state.health, min(
                        ARROWS_VALUES[-1], state.arrows+3), max(MATERIAL_VALUES[0], state.materials - 1), 1)))

        else:
            return None, None

        cost = 0
        for choice in choices:
            cost += choice[0] * (costs[ACTION_CRAFT] + REWARD[choice[1].show()])

        return cost, choices

    elif action_type == ACTION_GATHER:

        if state.materials == 2:
            return None, None

        choices = []
        if state.position == 2 and state.materials < 2:
            if state.mood == 0:
                choices.append((0.15, State(state.position, state.health, state.arrows, min(MATERIAL_VALUES[-1], state.materials + 1), 1)))
                choices.append((0.05, State(state.position, state.health, state.arrows, state.materials, 1)))
                choices.append((0.6, State(state.position, state.health, state.arrows, min(MATERIAL_VALUES[-1], state.materials + 1), 0)))
                choices.append((0.2, State(state.position, state.health, state.arrows, state.materials, 0)))
            elif state.mood == 1:
                if state.position == 1 or state.position == 4:
                    choices.append((0.5, State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0)))
                    REWARD[State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0).show()] = -40
                    choices.append((0.375, State(state.position, state.health, state.arrows, min(MATERIAL_VALUES[-1], state.materials + 1), 1)))
                    choices.append((0.125, State(state.position, state.health, state.arrows, state.materials, 1)))
                else:
                    choices.append((0.375, State(state.position, state.health, state.arrows, min(MATERIAL_VALUES[-1], state.materials + 1), 0)))
                    choices.append((0.125, State(state.position, state.health, state.arrows, state.materials, 0)))
                    choices.append((0.375, State(state.position, state.health, state.arrows, min(MATERIAL_VALUES[-1], state.materials + 1), 1)))
                    choices.append((0.125, State(state.position, state.health, state.arrows, state.materials, 1)))
        else:
            return None, None

        cost = 0
        for choice in choices:
            cost += choice[0] * (costs[ACTION_GATHER] + REWARD[choice[1].show()])

        return cost, choices

    elif action_type == ACTION_MOVE:

        cost = 10000000
        choices = []
        if state.position == 0:

            directions = [4, 0]
            for direction in directions:
                temp_cost = 0
                temp_choice = []

                if state.mood == 0:
                    temp_choice.append((0.17, State(direction, state.health, state.arrows, state.materials, 1)))
                    temp_choice.append((0.03, State(1, state.health, state.arrows, state.materials, 1)))
                    temp_choice.append((0.68, State(direction, state.health, state.arrows, state.materials, 0)))
                    temp_choice.append((0.12, State(1, state.health, state.arrows, state.materials, 0)))
                elif state.mood == 1:
                    temp_choice.append((0.425, State(direction, state.health, state.arrows, state.materials, 0)))
                    temp_choice.append((0.075, State(1, state.health, state.arrows, state.materials, 0)))
                    temp_choice.append((0.425, State(direction, state.health, state.arrows, state.materials, 1)))
                    temp_choice.append((0.075, State(1, state.health, state.arrows, state.materials, 1)))

                for choice in temp_choice:
                    temp_cost += choice[0] * (costs[ACTION_MOVE] + REWARD[choice[1].show()])

                if cost > temp_cost:
                    cost = temp_cost
                    choices = temp_choice

        elif state.position == 1:

            directions = [4, 1]
            for direction in directions:
                temp_cost = 0
                temp_choice = []

                if state.mood == 0:
                    temp_choice.append((0.2, State(direction, state.health, state.arrows, state.materials, 1)))
                    temp_choice.append((0.8, State(direction, state.health, state.arrows, state.materials, 0)))
                elif state.mood == 1:
                    temp_choice.append((0.5, State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0)))
                    REWARD[State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0).show()] = -40
                    temp_choice.append((0.5, State(direction, state.health, state.arrows, state.materials, 1)))

                for choice in temp_choice:
                    temp_cost += choice[0] * (costs[ACTION_MOVE] + REWARD[choice[1].show()])

                if cost > temp_cost:
                    cost = temp_cost
                    choices = temp_choice

        elif state.position == 2:

            directions = [4, 2]
            for direction in directions:
                temp_cost = 0
                temp_choice = []

                if state.mood == 0:
                    temp_choice.append((0.17, State(direction, state.health, state.arrows, state.materials, 1)))
                    temp_choice.append((0.03, State(1, state.health, state.arrows, state.materials, 1)))
                    temp_choice.append((0.68, State(direction, state.health, state.arrows, state.materials, 0)))
                    temp_choice.append((0.12, State(1, state.health, state.arrows, state.materials, 0)))
                elif state.mood == 1:
                    temp_choice.append((0.425, State(direction, state.health, state.arrows, state.materials, 1)))
                    temp_choice.append((0.425, State(1, state.health, state.arrows, state.materials, 1)))
                    temp_choice.append((0.425, State(direction, state.health, state.arrows, state.materials, 0)))
                    temp_choice.append((0.075, State(1, state.health, state.arrows, state.materials, 0)))

                for choice in temp_choice:
                    temp_cost += choice[0] * (costs[ACTION_MOVE] + REWARD[choice[1].show()])

                if cost > temp_cost:
                    cost = temp_cost
                    choices = temp_choice

        elif state.position == 3:

            directions = [4, 3]
            for direction in directions:
                temp_cost = 0
                temp_choice = []

                if state.mood == 0:
                    temp_choice.append((0.2, State(direction, state.health, state.arrows, state.materials, 1)))
                    temp_choice.append((0.8, State(direction, state.health, state.arrows, state.materials, 0)))
                elif state.mood == 1:
                    temp_choice.append((0.5, State(direction, state.health, state.arrows, state.materials, 0)))
                    temp_choice.append((0.5, State(direction, state.health, state.arrows, state.materials, 1)))

                for choice in temp_choice:
                    temp_cost += choice[0] * (costs[ACTION_MOVE] + REWARD[choice[1].show()])

                if cost > temp_cost:
                    cost = temp_cost
                    choices = temp_choice

        elif state.position == 4:

            directions = [0, 1, 2, 3, 4]
            for direction in directions:
                temp_cost = 0
                temp_choice = []

                if state.mood == 0:
                    temp_choice.append((0.17, State(direction, state.health, state.arrows, state.materials, 1)))
                    temp_choice.append((0.03, State(1, state.health, state.arrows, state.materials, 1)))
                    temp_choice.append((0.68, State(direction, state.health, state.arrows, state.materials, 0)))
                    temp_choice.append((0.12, State(1, state.health, state.arrows, state.materials, 0)))
                elif state.mood == 1:
                    temp_choice.append((0.5, State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0)))
                    REWARD[State(state.position, min(HEALTH_VALUES[-1], state.health+1), 0, state.materials, 0).show()] = -40
                    temp_choice.append((0.425, State(direction, state.health, state.arrows, state.materials, 1)))
                    temp_choice.append((0.075, State(1, state.health, state.arrows, state.materials, 1)))

                for choice in temp_choice:
                    temp_cost += choice[0] * (costs[ACTION_MOVE] + REWARD[choice[1].show()])

                if cost > temp_cost:
                    cost = temp_cost
                    choices = temp_choice

        return cost, choices

def show(i, utilities, policies, path):
    with open(path, 'a+') as f:
        f.write('iteration={}\n'.format(i))
        utilities = np.around(utilities, 3)
        for state, util in np.ndenumerate(utilities):
            state = State(*state)

            if state.health == 0:
                f.write('{}:-1=[{:.3f}]\n'.format(state, util))
                continue

            act_str = ""

            if policies[state.show()] == ACTION_SHOOT:
                act_str = 'SHOOT'
            elif policies[state.show()] == ACTION_HIT:
                act_str = 'HIT'
            elif policies[state.show()] == ACTION_CRAFT:
                act_str = 'CRAFT'
            elif policies[state.show()] == ACTION_GATHER:
                act_str = 'GATHER'
            elif policies[state.show()] == ACTION_MOVE:
                act_str = 'MOVE'

            f.write('{}:{}=[{:.3f}]\n'.format(state, act_str, util))
        f.write('\n\n')

def value_iteration(delta_inp, gamma_inp, costs_inp, path):
    utilities = np.zeros((POSITION_RANGE, HEALTH_RANGE, ARROWS_RANGE, MATERIAL_RANGE, MOOD_RANGE))
    policies = np.full((POSITION_RANGE, HEALTH_RANGE, ARROWS_RANGE, MATERIAL_RANGE, MOOD_RANGE), -1, dtype='int')

    index = 0
    done = False

    while not done:  # one iteration of value iteration
        #print(index)
        temp = np.zeros(utilities.shape)
        delta = np.NINF

        for state, util in np.ndenumerate(utilities):

            # print(state, util)
            if state[1] == 0:
                continue

            new_util = np.NINF
            for act_index in range(NUM_ACTIONS):
                cost, states = action(act_index, state, costs_inp)

                if cost is None:
                    continue

                # print(cost, states)
                expected_util = reduce(
                    add, map(lambda x: x[0]*utilities[x[1].show()], states))
                new_util = max(new_util, cost + gamma_inp * expected_util)

            temp[state] = new_util
            delta = max(delta, abs(util - new_util))

        utilities = deepcopy(temp)

        for state, _ in np.ndenumerate(utilities):
            if state[0] == 0:
                continue
            best_util = np.NINF
            best_action = None

            for act_index in range(NUM_ACTIONS):
                cost, states = action(act_index, state, costs_inp)

                if states is None:
                    continue

                action_util = cost + gamma_inp * \
                    reduce(
                        add, map(lambda x: x[0]*utilities[x[1].show()], states))

                if action_util > best_util:
                    best_action = act_index
                    best_util = action_util

            policies[state] = best_action

        show(index, utilities, policies, path)
        index += 1
        if delta < delta_inp:
            done = True
    return index

# PREP
os.makedirs('outputs', exist_ok=True)

# TASK 1
path = 'outputs/task_1_trace.txt'
value_iteration(DELTA, GAMMA, (COST, COST, COST, COST, COST), path)

# TASK 2 Case 3
path = 'outputs/task_2_3_trace.txt'
value_iteration(DELTA, 0.25, (COST, COST, COST, COST, COST), path)
