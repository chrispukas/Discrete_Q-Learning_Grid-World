from dataclasses import dataclass

import numpy as np


@dataclass
class Tile:
    weighted_value: int
    move_value: int


class Environment:
    def __init__(self):
        self.reward_table = self.create_reward_table()
        self.q_table = self.create_q_table()

    def create_reward_table(self):
        reward_table = np.array([[100, -1, -1, -1, -1],
                                  [-1, -99, -99, -1, -1],
                                  [-1, -99, -99, -1, -1],
                                  [-1, -1, -1, -1, -1],
                                  [-1, -1, -1, -1, -20],])
        return reward_table

    def get_reward(self, state):
        return self.reward_table[state[0]][state[1]]
    
    def get_q_values(self, state):
        return self.q_table[state].values()
    
    def get_q_value(self, state, action):
        return self.q_table[state][action]

    def print_reward_table(self):
        for row in self.reward_table:
            print('\n')
            for cell in row:
                print(self.ascii_cell_convert(cell), end=" ")

    def create_q_table(self):
        table = dict() # Create a nested dictionary
        dirs = {(0, +1), (0, -1), (+1, 0), (-1, 0)}

        for i, row in enumerate(self.reward_table):
            for j, _ in enumerate(row):
                table[(i,j)] = {}

                # Cleanup, allows only valid actions
                for dx, dy in dirs:
                    if is_coordinate_in_bounds(self.reward_table, (i + dx, j + dy)):
                        table[(i,j)][(dx, dy)] = 0
        return table
    
    def ascii_cell_convert(self, 
                           value: int) -> str:
       result = "#"
       match value:
           case 0:
               result = "S"
           case -1:
               result = "□"
           case -30:
               result = "■"
           case 100:
               result = "G"
       return result
    



def is_coordinate_in_bounds(reward_table, coordinate):
    env_height = len(reward_table)
    env_width = len(reward_table[0])

    if coordinate[0] < 0 or coordinate[1] < 0:
        return False  # Out of bounds
    elif coordinate[0] >= env_height or coordinate[1] >= env_width:
        return False  # Out of bounds
    return True
