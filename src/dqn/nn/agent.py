import random

import dqn.nn.environment as env

def run_agent(environment: env.Environment, 
              learning_rate: float=0.2, 
              exploration_probability: float=0.01, 
              gamma_discount: float=0.9,
              exponential_decay: float=0.99,
              max_timesteps_per_epoch: int=300,
              max_epochs: int=200) -> tuple[dict[dict], dict]:

    epoch_steps_pair = []

    # O(n^2) time, iterating through each epoch, refining the state table, until a stable solution is met
    for current_epoch in range(max_epochs):
        (state_action_pairs) = epoch(environment, 
                       learning_rate=learning_rate, 
                       exploration_probability=exploration_probability,
                       exponential_decay=exponential_decay,
                       gamma_discount=gamma_discount,
                       max_timesteps_per_epoch=max_timesteps_per_epoch)
        epoch_steps_pair.append((current_epoch, len(state_action_pairs)))

    return {"state_action_pairs": state_action_pairs, 
             "epoch_steps": epoch_steps_pair}

def epoch(environment: env.Environment, 
          learning_rate: float, 
          exploration_probability: float,
          exponential_decay: float, 
          gamma_discount: float,
          max_timesteps_per_epoch: int) -> tuple[dict[dict], list[dict]]:
    # Starting coordinate, representing the bottom right of the 2D array defined in the reward table
    current_coordinate = (4,4)
    state_action_pairs = []

    current_exploration_probability = exploration_probability

    # Timestep counter, until maximum time is reached
    for curr_timestep in range(max_timesteps_per_epoch):

        action, new_coordinate = timestep(environment, 
                                          current_coordinate, 
                                          exploration_probability=current_exploration_probability)
        state_action_pairs.append((current_coordinate, action))

        if new_coordinate == (0,0):
            #print(f"Reached goal in {curr_timestep} steps")
            break

        current_coordinate = new_coordinate
        current_exploration_probability *= exponential_decay # Exponential decay

    update_q_table(environment, 
                   state_action_pairs=state_action_pairs, 
                   learning_rate=learning_rate, 
                   gamma_discount=gamma_discount)

    return state_action_pairs


def timestep(environment: env.Environment, 
             current_coordinate: tuple[int, int], 
             exploration_probability: float) -> tuple[tuple[int, int], tuple[int, int]]:
    state = environment.q_table[current_coordinate]
    action = select_action(state, exploration_probability)
    new_coordinate = (current_coordinate[0] + action[0], current_coordinate[1] + action[1])

    return action, new_coordinate


def update_q_table(environment: env.Environment, 
                   state_action_pairs: list[tuple[tuple[int, int], tuple[int, int]]],
                   learning_rate: float,
                   gamma_discount: float) -> None:
    state_action_pairs.reverse()
    for i, (state, action) in enumerate(state_action_pairs):
        reward = environment.get_reward(state)

        # Get the next reward, apply bellman to the current reward
        #implemented q_learning formula
        if i == 0:
            next_max = 0
        else:
            next_state = state_action_pairs[i - 1][0]
            next_max = max(environment.get_q_values(next_state))

        old_value = environment.q_table[state][action]
        environment.q_table[state][action] += learning_rate * (reward + gamma_discount * next_max - old_value)


# Returns the new coordinate for the agent
def select_action(state, 
                  exploration_probability: float) -> tuple[int, int]:
    rand = random.random()
    if exploration_probability > rand:
        return random.choice(list(state.keys()))
    else:
        return max(state, key=state.get)