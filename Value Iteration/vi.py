import numpy as np
from copy import deepcopy
from functools import reduce
from operator import add
import os

HEALTH_RANGE = 5
ARROWS_RANGE = 4
MATERIAL_RANGE = 3
POSITION_RANGE = 5

HEALTH_VALUES = tuple(range(HEALTH_RANGE))
ARROWS_VALUES = tuple(range(ARROWS_RANGE))
MATERIAL_VALUES = tuple(range(MATERIAL_RANGE))
POSITION_VALUES = tuple(range(POSITION_RANGE))

HEALTH_FACTOR = 25 # 0, 25, 50, 75, 100
ARROWS_FACTOR = 1 # 0, 1, 2, 3
MATERIAL_FACTOR = 1 # 0, 1, 2
POSITION_FACTOR = 1 # (0, north), (1, east), (2, south), (3, west), (4, center)

NUM_ACTIONS = 5 # (move, shoot, hit), (move, craft), (move, gather), (move, shoot, hit), (move, shoot)
ACTION_MOVE = 0
ACTION_SHOOT = 1
ACTION_HIT = 2
ACTION_CRAFT = 3
ACTION_GATHER = 4

TEAM = 21
Y = 0.5
PRIZE = 50
COST = -20

GAMMA = 0.999
DELTA = 0.001

REWARD = np.zeros((HEALTH_RANGE, ARROWS_RANGE, MATERIAL_RANGE, POSITION_RANGE))
REWARD[0, :, :, :] = PRIZE
print(REWARD)

class State:
    def __init__(self, enemy_health, num_arrows, materials, position):
        if (enemy_health not in HEALTH_VALUES) or (num_arrows not in ARROWS_VALUES) or (materials not in MATERIAL_VALUES):
            raise ValueError

        self.position = position
        self.health = enemy_health
        self.arrows = num_arrows
        self.materials = materials

    def show(self):
        return (self.health, self.arrows, self.materials, self.position)

    def __str__(self):
        return f'({self.health},{self.arrows},{self.materials}, {self.position})'

def action(action_type, state, costs):
    # returns cost, array of tuple of (probability, state)

    state = State(*state)

    if action_type == ACTION_SHOOT:
        if state.arrows == 0:
            return None, None

        new_arrows = state.arrows - 1

        choices = []
        if state.position == 1:
            choices.append(
                (0.9, State(state.position, max(HEALTH_VALUES[0], state.health-1), new_arrows, state.materials)))
            choices.append((0.1, State(state.position, state.health, new_arrows, state.materials)))
        elif state.position == 3:
            choices.append(
                (0.25, State(state.position, max(HEALTH_VALUES[0], state.health-1), new_arrows, state.materials)))
            choices.append((0.75, State(state.position, state.health, new_arrows, state.materials)))
        elif state.position == 4:
            choices.append(
                (0.5, State(state.position, max(HEALTH_VALUES[0], state.health-1), new_arrows, state.materials)))
            choices.append((0.5, State(state.position, state.health, new_arrows, state.materials)))

        cost = 0
        for choice in choices:
            cost += choice[0] * (costs[ACTION_SHOOT] + REWARD[choice[1].show()])

        return cost, choices

    elif action_type == ACTION_HIT:
        choices = []
        if state.position == 1:
            choices.append(
                (0.2, State(state.position, max(HEALTH_VALUES[0], state.health-2), state.arrows, state.materials)))
            choices.append((0.8, State(state.position, state.health, new_arrows, state.materials)))
        elif state.position == 4:
            choices.append(
                (0.1, State(state.position, max(HEALTH_VALUES[0], state.health-2), state.arrows, state.materials)))
            choices.append((0.9, State(state.position, state.health, new_arrows, state.materials)))

        cost = 0
        for choice in choices:
            cost += choice[0] * (costs[ACTION_HIT] + REWARD[choice[1].show()])

        return cost, choices

    elif action_type == ACTION_CRAFT:
        if state.materials == 0:
            return None, None

        choices = []
        if state.position == 0 and state.materials > 0 and state.arrows < 3:
            choices.append((0.5, State(state.position, state.health, min(
                ARROWS_VALUES[-1], state.arrows+1), max(MATERIAL_VALUES[0], state.materials - 1))))
            choices.append((0.35, State(state.position, state.health, min(
                ARROWS_VALUES[-1], state.arrows+2), max(MATERIAL_VALUES[0], state.materials - 1))))
            choices.append((0.15, State(state.position, state.health, min(
                ARROWS_VALUES[-1], state.arrows+3), max(MATERIAL_VALUES[0], state.materials - 1))))

        cost = 0
        for choice in choices:
            cost += choice[0] * (costs[ACTION_CRAFT] + REWARD[choice[1].show()])

        return cost, choices

    elif action_type == ACTION_GATHER:

        if state.materials == 2:
            return None, None

        choices = []
        if state.position == 2 and state.materials < 2:
            choices.append((0.75, State(state.position, state.health, state.arrows, min(MATERIAL_VALUES[-1], state.materials + 1))))
            choices.append((0.25, State(state.position, state.health, state.arrows, state.materials)))

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

                temp_choice.append((0.85, State(direction, state.health, state.arrows, state.materials)))
                temp_choice.append((0.15, State(1, state.health, state.arrows, state.materials)))

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

                temp_choice.append((1, State(direction, state.health, state.arrows, state.materials)))

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

                temp_choice.append((0.85, State(direction, state.health, state.arrows, state.materials)))
                temp_choice.append((0.15, State(1, state.health, state.arrows, state.materials)))

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

                temp_choice.append((1, State(direction, state.health, state.arrows, state.materials)))

                for choice in temp_choice:
                    temp_choice += choice[0] * (costs[ACTION_MOVE] + REWARD[choice[1].show()])

                if cost > temp_cost:
                    cost = temp_cost
                    choices = temp_choice

        elif state.position == 4:

            directions = [0, 1, 2, 3, 4]
            for direction in directions:
                temp_cost = 0
                temp_choice = []

                temp_choice.append((0.85, State(direction, state.health, state.arrows, state.materials)))
                temp_choice.append((0.15, State(1, state.health, state.arrows, state.materials)))

                for choice in temp_choice:
                    temp_cost += choice[0] * (costs[ACTION_MOVE] + REWARD[choice[1].show()])

                if cost < temp_cost:
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
    utilities = np.zeros((HEALTH_RANGE, ARROWS_RANGE, MATERIAL_RANGE, POSITION_RANGE))
    policies = np.full((HEALTH_RANGE, ARROWS_RANGE,
                        MATERIAL_RANGE, POSITION_RANGE), -1, dtype='int')

    index = 0
    done = False
    while not done:  # one iteration of value iteration
        #print(index)
        temp = np.zeros(utilities.shape)
        delta = np.NINF

        for state, util in np.ndenumerate(utilities):

            if state[0] == 0:
                continue
            new_util = np.NINF
            for act_index in range(NUM_ACTIONS):
                cost, states = action(act_index, state,costs_inp)

                if cost is None:
                    continue
                print(state, cost)
                print(list(map(lambda x: x[0]*utilities[x[1].show()], states)))
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
                cost, states = action(act_index, state, costs_inp )

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
value_iteration(DELTA, GAMMA, (COST,COST,COST, COST, COST), path)
