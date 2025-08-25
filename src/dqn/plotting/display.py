import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import dqn.nn.environment as env

def plot_epochs(pairs):
    x_vals, y_vals = zip(*pairs)
    plt.plot(x_vals, np.log(np.array(y_vals)))

    # Labels and title
    plt.xlabel("# of Epochs")
    plt.ylabel("# of Steps")
    plt.title("Epoch-Steps Plot")
    plt.legend()

    # Show the graph
    plt.grid(True)
    plt.show()


def plot_heatmap(data):
    sns.heatmap(data, cmap="viridis", annot=True, fmt=".2f")
    plt.title("State Value Heatmap (max Q over actions)")
    plt.show()



