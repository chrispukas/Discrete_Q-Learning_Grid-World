import dqn.src.agent as agent
import tkinter as tk

from dqn.src.display import plot_epochs
from dqn.src.environment import create_reward_table, print_env



reward_table = create_reward_table()
print_env(reward_table)
result, metrics = agent.run_agent(reward_table)


plot_epochs(metrics)



state_action_pairs = result[1]

root = tk.Tk()
root.title('display')
square_size = 50

for row in range(5):
    for col in range(5):

        reward_value = reward_table[row][col]
        match reward_value:
            case 100:
                colour = "green"
            case -99:
                colour = "red"
            case -20:
                colour = "blue"
            case _:
                colour = "lightgray"
        if any((row, col) in pair for pair in state_action_pairs):
            colour = "yellow"

        square = tk.Label(root, width=square_size // 10, height=square_size // 15, bg=colour, borderwidth=1,
                          relief="solid")
        square.grid(row=row, column=col, padx=1, pady=1)

root.mainloop()