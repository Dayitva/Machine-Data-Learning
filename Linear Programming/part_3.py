import os
import cvxpy as cp
import numpy as np

POSITION_RANGE = 5
MATERIAL_RANGE = 3
ARROWS_RANGE = 4
MOOD_RANGE = 2
HEALTH_RANGE = 5
NUM_STATES = 600 # (5 * 3 * 4 * 2 * 5)

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

class State:
    def __init__(self, position, materials, arrows, mood, enemy_health):
        self.position = position
        self.materials = materials
        self.arrows = arrows
        self.mood = mood
        self.health = enemy_health

    def show(self):
        return (self.position, self.materials, self.arrows, self.mood, self.health)
    
    def pos(self):
        return (self.position * (MATERIAL_RANGE * ARROWS_RANGE * MOOD_RANGE * HEALTH_RANGE) +
                self.materials * (ARROWS_RANGE * MOOD_RANGE * HEALTH_RANGE) +
                self.arrows * (MOOD_RANGE * HEALTH_RANGE) +
                self.mood * (HEALTH_RANGE) +
                self.health)
        
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
            
    def take_action(self, action):    
        if action == ACTION_NONE:
            return []
        
        elif action == ACTION_MOVE_UP:
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
            if self.position == 2 and self.materials < 2:
                return 1
            else:
                return 0
            
for i in range(POSITION_RANGE):
    for j in range(MATERIAL_RANGE):
        for k in range(ARROWS_RANGE):
            for l in range(MOOD_RANGE):
                for m in range(HEALTH_RANGE):
                    for n in range(NUM_ACTIONS):
                        VALID_PAIRS += State(i,j,k,l,m).check_valid_action(n)
                        
print(VALID_PAIRS)
                        
x = cp.Variable(VALID_PAIRS, name="x")
A = np.zeros((NUM_STATES, VALID_PAIRS), dtype=np.float64)

alpha = np.zeros((VALID_PAIRS, 1))
alpha[State(4,2,3,1,100).pos()][0] = 1.0

constraints = [cp.matmul(A, x) == alpha, x>=0]
objective = cp.Maximize(cp.matmul(R, x))
problem = cp.Problem(objective, constraints)
solution = problem.solve()

print(solution)
print(x.value)

os.makedirs("outputs", exist_ok=True)

