import tkinter as tk
import matplotlib.pyplot as plt

import numpy as np



def plot_epochs(metrics):
    epoch_steps_pair = metrics["epoch_steps"]

    keys = list(epoch_steps_pair.keys())
    values = list(epoch_steps_pair.values())

    plt.plot(keys, np.log(np.array(values)))

    # Labels and title
    plt.xlabel("epochs")
    plt.ylabel("steps")
    plt.title("epoch-steps plot")
    plt.legend()

    # Show the graph
    plt.grid(True)
    plt.show()




