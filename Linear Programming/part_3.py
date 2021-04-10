import os
import cvxpy as cp
import numpy as np

POSITION_RANGE = 5
MATERIAL_RANGE = 3
ARROWS_RANGE = 4
MOOD_RANGE = 2
HEALTH_RANGE = 5
NUM_STATES = 600 # (5 * 3 * 4 * 2 * 5)

HEALTH_VALUES = tuple(range(HEALTH_RANGE)) # 0, 25, 50, 75, 100
ARROWS_VALUES = tuple(range(ARROWS_RANGE)) # 0, 1, 2, 3
MATERIAL_VALUES = tuple(range(MATERIAL_RANGE)) # 0, 1, 2
POSITION_VALUES = tuple(range(POSITION_RANGE)) # (0, north), (1, east), (2, south), (3, west), (4, center)
MOOD_VALUES = tuple(range(MOOD_RANGE)) # (0, dormant), (1, ready)

POSITION_ARRAY = ["N", "E", "S", "W", "C"]
HEALTH_ARRAY = [0, 25, 50, 75, 100]
MOOD_ARRAY = ["D", "R"]
MOVE_ARRAY = ["UP", "DOWN", "LEFT", "RIGHT", "STAY"]

NUM_ACTIONS = 10 # move_up, move_right, move_down, move_right, stay, shoot, hit, craft, gather
ACTION_MOVE_UP = 0
ACTION_MOVE_RIGHT = 1
ACTION_MOVE_DOWN = 2
ACTION_MOVE_LEFT = 3
ACTION_STAY = 4
ACTION_SHOOT = 5
ACTION_HIT = 6
ACTION_CRAFT = 7
ACTION_GATHER = 8
ACTION_NONE = 9

VALID_PAIRS = 0
PUNISHMENT = -40
COST = -20
REWARD = np.zeros((POSITION_RANGE, HEALTH_RANGE, ARROWS_RANGE, MATERIAL_RANGE, MOOD_RANGE))

class State:
    def __init__(self, position, enemy_health, arrows, materials, mood):
        self.position = position
        self.materials = materials
        self.arrows = arrows
        self.mood = mood
        self.health = enemy_health

    def show(self):
        return (self.position, self.health, self.arrows, self.materials, self.mood)

    def pos(self):
        return (self.position * (HEALTH_RANGE * ARROWS_RANGE * MATERIAL_RANGE * MOOD_RANGE) +
                self.health * (ARROWS_RANGE * MATERIAL_RANGE * MOOD_RANGE) +
                self.arrows * (MATERIAL_RANGE * MOOD_RANGE) +
                self.materials * (MOOD_RANGE) +
                self.mood)

    def check_valid_action(self, action):
        if action == ACTION_NONE:
            if self.health == 0:
                return 1
            else:
                return 0

        if self.health == 0:
            return 0

        if action == ACTION_MOVE_UP:
            if self.position == 2 or self.position == 4:
                return 1
            else:
                return 0

        elif action == ACTION_MOVE_RIGHT:
            if self.position == 3 or self.position == 4:
                return 1
            else:
                return 0

        elif action == ACTION_MOVE_DOWN:
            if self.position == 0 or self.position == 4:
                return 1
            else:
                return 0

        elif action == ACTION_MOVE_LEFT:
            if self.position == 1 or self.position == 4:
                return 1
            else:
                return 0

        elif action == ACTION_STAY:
            return 1

        elif action == ACTION_SHOOT:
            if (self.position == 1 or self.position == 3 or self.position == 4) and self.arrows > 0:
                return 1
            else:
                return 0

        elif action == ACTION_HIT:
            if self.position == 1 or self.position == 4:
                return 1
            else:
                return 0

        elif action == ACTION_CRAFT:
            if self.position == 0 and self.materials > 0:
                return 1
            else:
                return 0

        elif action == ACTION_GATHER:
            if self.position == 2:
                return 1
            else:
                return 0

    def take_action(self, action, idx):
        if action == ACTION_NONE:
            return []

        elif action == ACTION_MOVE_UP:
            choices = []
            if self.position == 2:
                if self.mood == 0:
                    choices.append((0.17, State(4, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.03, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.68, State(4, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.12, State(1, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.425, State(4, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.075, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.425, State(4, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.175, State(1, self.health, self.arrows, self.materials, 0)))
            elif self.position == 4:
                if self.mood == 0:
                    choices.append((0.17, State(0, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.03, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.68, State(0, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.12, State(1, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.5, State(self.position, min(HEALTH_VALUES[-1], self.health+1), 0, self.materials, 0)))
                    choices.append((0.425, State(0, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.075, State(1, self.health, self.arrows, self.materials, 1)))

            return choices

        elif action == ACTION_MOVE_RIGHT:
            choices = []
            if self.position == 3:
                if self.mood == 0:
                    choices.append((0.2, State(4, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.8, State(4, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.5, State(4, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.5, State(4, self.health, self.arrows, self.materials, 0)))
            elif self.position == 4:
                if self.mood == 0:
                    choices.append((0.17, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.03, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.68, State(1, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.12, State(1, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.5, State(self.position, min(HEALTH_VALUES[-1], self.health+1), 0, self.materials, 0)))
                    choices.append((0.425, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.075, State(1, self.health, self.arrows, self.materials, 1)))

            return choices

        elif action == ACTION_MOVE_DOWN:
            choices = []
            if self.position == 0:
                if self.mood == 0:
                    choices.append((0.17, State(4, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.03, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.68, State(4, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.12, State(1, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.425, State(4, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.075, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.425, State(4, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.175, State(1, self.health, self.arrows, self.materials, 0)))
            elif self.position == 4:
                if self.mood == 0:
                    choices.append((0.17, State(3, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.03, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.68, State(3, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.12, State(1, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.5, State(self.position, min(HEALTH_VALUES[-1], self.health+1), 0, self.materials, 0)))
                    choices.append((0.425, State(3, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.075, State(1, self.health, self.arrows, self.materials, 1)))

            return choices

        elif action == ACTION_MOVE_LEFT:
            choices = []
            if self.position == 1:
                if self.mood == 0:
                    choices.append((0.2, State(4, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.8, State(4, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.5, State(self.position, min(HEALTH_VALUES[-1], self.health+1), 0, self.materials, 0)))
                    choices.append((0.5, State(4, self.health, self.arrows, self.materials, 1)))
            elif self.position == 4:
                if self.mood == 0:
                    choices.append((0.17, State(3, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.03, State(3, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.68, State(3, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.12, State(3, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.5, State(self.position, min(HEALTH_VALUES[-1], self.health+1), 0, self.materials, 0)))
                    choices.append((0.425, State(3, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.075, State(3, self.health, self.arrows, self.materials, 1)))

            return choices

        elif action == ACTION_STAY:
            choices = []
            if self.position == 0:
                if self.mood == 0:
                    choices.append((0.17, State(0, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.03, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.68, State(0, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.12, State(1, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.425, State(0, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.075, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.425, State(0, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.175, State(1, self.health, self.arrows, self.materials, 0)))
            elif self.position == 1:
                if self.mood == 0:
                    choices.append((0.2, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.8, State(1, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.5, State(self.position, min(HEALTH_VALUES[-1], self.health+1), 0, self.materials, 0)))
                    choices.append((0.5, State(1, self.health, self.arrows, self.materials, 1)))
            elif self.position == 2:
                if self.mood == 0:
                    choices.append((0.17, State(2, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.03, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.68, State(2, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.12, State(1, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.425, State(2, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.075, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.425, State(2, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.175, State(1, self.health, self.arrows, self.materials, 0)))
            elif self.position == 3:
                if self.mood == 0:
                    choices.append((0.2, State(3, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.8, State(3, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.5, State(3, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.5, State(3, self.health, self.arrows, self.materials, 1)))
            elif self.position == 4:
                if self.mood == 0:
                    choices.append((0.17, State(4, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.03, State(1, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.68, State(4, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.12, State(1, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.5, State(self.position, min(HEALTH_VALUES[-1], self.health+1), 0, self.materials, 0)))
                    choices.append((0.425, State(4, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.075, State(1, self.health, self.arrows, self.materials, 1)))

            return choices

        elif action == ACTION_SHOOT:
            if state.arrows == 0:
                return []

            new_arrows = self.arrows - 1

            choices = []
            if self.arrows > 0:
                if self.position == 1:
                    if self.mood == 0:
                        choices.append(
                            (0.18, State(self.position, max(HEALTH_VALUES[0], self.health-1), new_arrows, self.materials, 1)))
                        choices.append((0.02, State(self.position, self.health, new_arrows, self.materials, 1)))
                        choices.append(
                            (0.72, State(self.position, max(HEALTH_VALUES[0], self.health-1), new_arrows, self.materials, 0)))
                        choices.append((0.08, State(self.position, self.health, new_arrows, self.materials, 0)))
                    elif self.mood == 1:
                        choices.append((0.5, State(self.position, min(HEALTH_VALUES[-1], self.health+1), 0, self.materials, 0)))
                        choices.append((0.45, State(self.position, max(HEALTH_VALUES[0], self.health-1), new_arrows, self.materials, 1)))
                        choices.append((0.05, State(self.position, self.health, new_arrows, self.materials, 1)))

                elif self.position == 3:
                    if self.mood == 0:
                        choices.append(
                            (0.05, State(self.position, max(HEALTH_VALUES[0], self.health-1), new_arrows, self.materials, 1)))
                        choices.append((0.15, State(self.position, self.health, new_arrows, self.materials, 1)))
                        choices.append(
                            (0.2, State(self.position, max(HEALTH_VALUES[0], self.health-1), new_arrows, self.materials, 0)))
                        choices.append((0.6, State(self.position, self.health, new_arrows, self.materials, 0)))
                    elif self.mood == 1:
                        choices.append((0.125, State(self.position, max(HEALTH_VALUES[0], self.health-1), new_arrows, self.materials, 0)))
                        choices.append((0.375, State(self.position, self.health, new_arrows, self.materials, 0)))
                        choices.append((0.125, State(self.position, max(HEALTH_VALUES[0], self.health-1), new_arrows, self.materials, 1)))
                        choices.append((0.375, State(self.position, self.health, new_arrows, self.materials, 1)))

                elif self.position == 4:
                    if self.mood == 0:
                        choices.append(
                            (0.1, State(self.position, max(HEALTH_VALUES[0], self.health-1), new_arrows, self.materials, 1)))
                        choices.append((0.1, State(self.position, self.health, new_arrows, self.materials, 1)))
                        choices.append(
                            (0.4, State(self.position, max(HEALTH_VALUES[0], self.health-1), new_arrows, self.materials, 0)))
                        choices.append((0.4, State(self.position, self.health, new_arrows, self.materials, 0)))
                    elif self.mood == 1:
                        choices.append((0.5, State(self.position, min(HEALTH_VALUES[-1], self.health+1), 0, self.materials, 0)))
                        choices.append((0.25, State(self.position, max(HEALTH_VALUES[0], self.health-1), 0, self.materials, 1)))
                        choices.append((0.25, State(self.position, self.health, 0, self.materials, 1)))

            return choices

        elif action == ACTION_HIT:
            choices = []

            if self.position == 1:
                if self.mood == 0:
                    choices.append(
                        (0.04, State(self.position, max(HEALTH_VALUES[0], self.health-2), self.arrows, self.materials, 1)))
                    choices.append((0.16, State(self.position, self.health, self.arrows, self.materials, 1)))
                    choices.append(
                        (0.16, State(self.position, max(HEALTH_VALUES[0], self.health-2), self.arrows, self.materials, 0)))
                    choices.append((0.64, State(self.position, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.5, State(self.position, min(HEALTH_VALUES[-1], self.health+1), 0, self.materials, 0)))
                    choices.append((0.1, State(self.position, max(HEALTH_VALUES[0], self.health-2), self.arrows, self.materials, 1)))
                    choices.append((0.4, State(self.position, self.health, self.arrows, self.materials, 1)))

            elif self.position == 4:
                if self.mood == 0:
                    choices.append(
                        (0.02, State(self.position, max(HEALTH_VALUES[0], self.health-2), self.arrows, self.materials, 1)))
                    choices.append((0.18, State(self.position, self.health, self.arrows, self.materials, 1)))
                    choices.append(
                        (0.08, State(self.position, max(HEALTH_VALUES[0], self.health-2), self.arrows, self.materials, 0)))
                    choices.append((0.72, State(self.position, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.5, State(self.position, min(HEALTH_VALUES[-1], self.health+1), 0, self.materials, 0)))
                    choices.append(
                        (0.05, State(self.position, max(HEALTH_VALUES[0], self.health-2), self.arrows, self.materials, 1)))
                    choices.append((0.45, State(self.position, self.health, self.arrows, self.materials, 1)))

            return choices

        elif action == ACTION_CRAFT:
            choices = []
            if self.position == 0 and self.materials > 0:
                if self.mood == 0:
                    choices.append((0.1, State(self.position, self.health, min(
                        ARROWS_VALUES[-1], self.arrows+1), max(MATERIAL_VALUES[0], self.materials - 1), 1)))
                    choices.append((0.07, State(self.position, self.health, min(
                        ARROWS_VALUES[-1], self.arrows+2), max(MATERIAL_VALUES[0], self.materials - 1), 1)))
                    choices.append((0.03, State(self.position, self.health, min(
                        ARROWS_VALUES[-1], self.arrows+3), max(MATERIAL_VALUES[0], self.materials - 1), 1)))
                    choices.append((0.4, State(self.position, self.health, min(
                        ARROWS_VALUES[-1], self.arrows+1), max(MATERIAL_VALUES[0], self.materials - 1), 0)))
                    choices.append((0.28, State(self.position, self.health, min(
                        ARROWS_VALUES[-1], self.arrows+2), max(MATERIAL_VALUES[0], self.materials - 1), 0)))
                    choices.append((0.12, State(self.position, self.health, min(
                        ARROWS_VALUES[-1], self.arrows+3), max(MATERIAL_VALUES[0], self.materials - 1), 0)))
                elif self.mood == 1:
                    choices.append((0.25, State(self.position, self.health, min(
                        ARROWS_VALUES[-1], self.arrows+1), max(MATERIAL_VALUES[0], self.materials - 1), 0)))
                    choices.append((0.175, State(self.position, self.health, min(
                        ARROWS_VALUES[-1], self.arrows+2), max(MATERIAL_VALUES[0], self.materials - 1), 0)))
                    choices.append((0.075, State(self.position, self.health, min(
                        ARROWS_VALUES[-1], self.arrows+3), max(MATERIAL_VALUES[0], self.materials - 1), 0)))
                    choices.append((0.25, State(self.position, self.health, min(
                        ARROWS_VALUES[-1], self.arrows+1), max(MATERIAL_VALUES[0], self.materials - 1), 1)))
                    choices.append((0.175, State(self.position, self.health, min(
                        ARROWS_VALUES[-1], self.arrows+2), max(MATERIAL_VALUES[0], self.materials - 1), 1)))
                    choices.append((0.075, State(self.position, self.health, min(
                        ARROWS_VALUES[-1], self.arrows+3), max(MATERIAL_VALUES[0], self.materials - 1), 1)))

            return choices

        elif action == ACTION_GATHER:
            choices = []
            if self.position == 2:
                if self.mood == 0:
                    choices.append((0.15, State(self.position, self.health, self.arrows, min(MATERIAL_VALUES[-1], self.materials + 1), 1)))
                    choices.append((0.05, State(self.position, self.health, self.arrows, self.materials, 1)))
                    choices.append((0.6, State(self.position, self.health, self.arrows, min(MATERIAL_VALUES[-1], self.materials + 1), 0)))
                    choices.append((0.2, State(self.position, self.health, self.arrows, self.materials, 0)))
                elif self.mood == 1:
                    choices.append((0.375, State(self.position, self.health, self.arrows, min(MATERIAL_VALUES[-1], self.materials + 1), 0)))
                    choices.append((0.125, State(self.position, self.health, self.arrows, self.materials, 0)))
                    choices.append((0.375, State(self.position, self.health, self.arrows, min(MATERIAL_VALUES[-1], self.materials + 1), 1)))
                    choices.append((0.125, State(self.position, self.health, self.arrows, self.materials, 1)))

            return choices

valid_actions = [[] for i in range(600)]

for i in range(POSITION_RANGE):
    for j in range(HEALTH_RANGE):
        for k in range(ARROWS_RANGE):
            for l in range(MATERIAL_RANGE):
                for m in range(MOOD_RANGE):
                    for n in range(NUM_ACTIONS):
                        state = State(i,j,k,l,m)
                        if state.check_valid_action(n):
                            valid_actions[state.pos()].append(n)
                            VALID_PAIRS += 1

print(VALID_PAIRS)

x = cp.Variable((VALID_PAIRS, 1), name="x")
A = np.zeros((NUM_STATES, VALID_PAIRS), dtype=np.float64)
R = np.ones((1, VALID_PAIRS)) * COST
alpha = np.zeros((NUM_STATES, 1))
alpha[State(4,4,3,2,1).pos()][0] = 1.0

idx = 0
for i in range(POSITION_RANGE):
    for j in range(HEALTH_RANGE):
        for k in range(ARROWS_RANGE):
            for l in range(MATERIAL_RANGE):
                for m in range(MOOD_RANGE):
                    state = State(i,j,k,l,m)
                    for o in valid_actions[state.pos()]:
                        A[state.pos()][idx] += 1
                        next_states = state.take_action(o, idx)

                        for next_state in next_states:
                            A[next_state[1].pos()][idx] -= next_state[0]

                        idx += 1

idx = 0
for i in range(POSITION_RANGE):
    for j in range(HEALTH_RANGE):
        for k in range(ARROWS_RANGE):
            for l in range(MATERIAL_RANGE):
                for m in range(MOOD_RANGE):
                    state = State(i,j,k,l,m)
                    if state.health == 0:
                        R[0][idx] = 0
                        idx += 1
                        continue
                    for o in valid_actions[state.pos()]:
                        if state.mood == 1 and (state.position == 1 or state.position == 4):
                            R[0][idx] += 0.5*PUNISHMENT
                        idx += 1

constraints = [cp.matmul(A, x) == alpha, x>=0]
objective = cp.Maximize(cp.matmul(R, x))
problem = cp.Problem(objective, constraints)
solution = problem.solve()

print(solution)
print(x.value)
print(np.unique(A, return_counts=True))

os.makedirs("outputs", exist_ok=True)
