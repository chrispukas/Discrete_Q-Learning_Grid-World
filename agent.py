import random

from environment import print_env

# ------------------------------
# -- CONFIGURATION PARAMETERS --
# ------------------------------

learning_rate = 0.2
exploration_probability = 0.9
max_timestep_per_epoc = 200
max_epochs = 800

# ----------
# -- VARS --
# ----------

current_timestep = 0
current_epoch = 0

state_table = []



# ---------------
# -- FUNCTIONS --
# ---------------

def run_agent(reward_table):
    # Creating a state table, to keep track of the rewards based on a specific state
    global state_table
    state_table = create_state_table()

    result = None

    # O(n^2) time, iterating through each epoch, refining the state table, until a stable solution is met
    for counter in range(max_epochs):
       global current_epoch
       current_epoch = counter
       result = epoch(reward_table)

    return result

def epoch(reward_table):
    print(f"epoch {current_epoch}")

    # Starting coordinate, representing the bottom right of the 2D array defined in the state table
    current_coordinate = (4,4)
    path_taken = []

    # Timestep counter, until maximum time is reached
    for counter in range(max_timestep_per_epoc):
        global current_timestep
        current_timestep = counter
        current_coordinate = timestep(reward_table, current_coordinate)

        if current_coordinate == (0,0):
            break

        path_taken.append(current_coordinate)

    update_state_table(reward_table, path_taken)
    print(state_table)
    print(path_taken)

    return [state_table,path_taken]


def timestep(reward_table, current_coordinate):
    lookup = get_q_values_for_coordinate(reward_table, current_coordinate)
    action = select_action(lookup, exploration_probability)
    new_coordinate = (current_coordinate[0] + action[0], current_coordinate[1] + action[1])
    print(f"Selected {new_coordinate}")
    return new_coordinate
def update_state_table(reward_table, path_taken):

    path_taken.reverse()
    current_reward = reward_table[path_taken[0][0]][path_taken[0][1]]

    for step in path_taken:
        state_table[step[0]][step[1]] = current_reward
        current_reward = current_reward + reward_table[step[0]][step[1]]



# Returns the new coordinate for the agent
def select_action(lookup, exploration):
    rand = random.random()

    # Prune data, removing all occurrences of -999
    pruned_data = {k: v for k, v in lookup.items() if v != -999}

    if exploration < rand:
        return random.choice(list(pruned_data.keys()))
    else:
        max_val = max(pruned_data.values())
        max_keys = [k for k, v in pruned_data.items() if v == max_val]
        return random.choice(max_keys)

def get_q_values_for_coordinate(reward_table, current_coordinate):
    # Look up, down, left, and right from the current coordinate, to determine the optimum path to take.

    up_val = get_coordinate_q_value(current_coordinate, (0, +1))
    down_val = get_coordinate_q_value(current_coordinate, (0, -1))
    left_val = get_coordinate_q_value(current_coordinate, (-1, 0))
    right_val = get_coordinate_q_value(current_coordinate, (+1, 0))

    # in the format [UP, DOWN, LEFT, RIGHT]
    return {(0, 1): up_val, (0, -1): down_val, (-1, 0): left_val, (+1,0): right_val}

def get_coordinate_q_value(current_coordinate, target_coordinate):
    new_coordinate = [current_coordinate[0] + target_coordinate[0], current_coordinate[1] + target_coordinate[1]]
    in_bounds = is_coordinate_in_bounds(new_coordinate)
    if not in_bounds:
        return -999
    return state_table[new_coordinate[0]][new_coordinate[1]] # Within Bounds

def create_state_table():
    table = \
        [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        ]
    return table

def is_coordinate_in_bounds(coordinate):
    global state_table
    env_height = len(state_table)
    env_width = len(state_table[0])

    if coordinate[0] < 0 or coordinate[1] < 0:
        print(f"Coordinate out of bounds! {coordinate}")
        return False  # Out of bounds
    elif coordinate[0] >= env_height or coordinate[1] >= env_width:
        print(f"Coordinate out of bounds! {coordinate}")
        return False  # Out of bounds
    return True
