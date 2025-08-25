import random

# ------------------------------
# -- CONFIGURATION PARAMETERS --
# ------------------------------

learning_rate = 0.2
exploration_probability = 0.01
gamma_discount = 0.9

max_timestep_per_epoc = 300
max_epochs = 200

# -------------
# -- METRICS --
# -------------

epoch_steps_pair = dict()

# ----------
# -- VARS --
# ----------

current_timestep = 0
current_epoch = 0

q_table = dict(dict())



# ---------------
# -- FUNCTIONS --
# ---------------

def run_agent(reward_table):
    # Creating a state table, to keep track of the rewards based on a specific state
    global q_table
    q_table = create_q_table(reward_table)

    result = None

    # O(n^2) time, iterating through each epoch, refining the state table, until a stable solution is met
    for counter in range(max_epochs):
        global current_epoch
        current_epoch = counter
        result = epoch(reward_table)

        epoch_steps_pair[current_epoch] = len(result[1])

    return result, {"epoch_steps": epoch_steps_pair}





def epoch(reward_table):
    print(f"epoch {current_epoch}")

    # Starting coordinate, representing the bottom right of the 2D array defined in the reward table
    current_coordinate = (4,4)
    state_action_pairs = []

    global current_timestep

    # Timestep counter, until maximum time is reached
    for current_timestep in range(max_timestep_per_epoc):

        action, new_coordinate = timestep(current_coordinate)
        state_action_pairs.append({current_coordinate: action})

        if new_coordinate == (0,0):
            print(f"Reached goal in {current_timestep} steps")
            break

        current_coordinate = new_coordinate

    update_q_table(reward_table, state_action_pairs)
    print(state_action_pairs)

    return [q_table, state_action_pairs]


def timestep(current_coordinate):
    global q_table
    state = q_table[current_coordinate]
    action = select_action(state, exploration_probability)
    new_coordinate = (current_coordinate[0] + action[0], current_coordinate[1] + action[1])

    return action, new_coordinate


def update_q_table(reward_table, state_action_pairs):
    global q_table
    state_action_pairs.reverse()

    for pairid, pair in enumerate(state_action_pairs):
        state = list(pair.keys())[0]
        action = list(pair.values())[0]

        reward = reward_table[state[0]][state[1]]

        #implemented q_learning formula
        if pairid == 0:
            next_max = 0
        else:
            next_state = list(state_action_pairs[pairid - 1].keys())[0]
            next_max = max(q_table[next_state].values())

        old_value = q_table[state][action]
        q_table[state][action] += learning_rate * (reward + gamma_discount * next_max - old_value)


# Returns the new coordinate for the agent
def select_action(state, exploration_probability):
    rand = random.random()
    if exploration_probability > rand:
        return random.choice(list(state.keys()))
    else:
        return max(state, key=state.get)

def create_q_table(reward_table):
    table = dict() # Create a nested dictionary

    dirs = {(0, +1), (0, -1), (+1, 0), (-1, 0)}

    for i, row in enumerate(reward_table):
        for j, _ in enumerate(row):
            table[(i,j)] = {}

            # Cleanup, allows only valid actions
            for dx, dy in dirs:
                if is_coordinate_in_bounds(reward_table, (i + dx, j + dy)):
                    table[(i,j)][(dx, dy)] = 0
    return table

def is_coordinate_in_bounds(reward_table, coordinate):
    env_height = len(reward_table)
    env_width = len(reward_table[0])

    if coordinate[0] < 0 or coordinate[1] < 0:
        print(f"Coordinate out of bounds! {coordinate}")
        return False  # Out of bounds
    elif coordinate[0] >= env_height or coordinate[1] >= env_width:
        print(f"Coordinate out of bounds! {coordinate}")
        return False  # Out of bounds
    return True
