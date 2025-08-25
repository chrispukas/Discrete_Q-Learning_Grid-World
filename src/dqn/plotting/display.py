import matplotlib.pyplot as plt
import numpy as np

import dqn.nn.environment as env

def plot_epochs(pairs):
    x_vals, y_vals = zip(*pairs)
    plt.plot(x_vals, np.log(np.array(y_vals)))

    # Labels and title
    plt.xlabel("epochs")
    plt.ylabel("steps")
    plt.title("epoch-steps plot")
    plt.legend()

    # Show the graph
    plt.grid(True)
    plt.show()


def plot_heatmap(data):
    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title("Q-Table Heatmap")
    plt.xlabel("Actions")
    plt.ylabel("States")
    plt.show()


def plot_map(environment: env.Environment, 
             state_action_pairs: list[tuple[int, int]]):
    pass



