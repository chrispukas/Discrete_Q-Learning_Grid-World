import agent
import tkinter as tk
from environment import create_reward_table, print_env


def main():
    print("init")


if __name__ == "__main__":
    main()



reward_table = create_reward_table()
print_env(reward_table)

result = agent.run_agent(reward_table)

root = tk.Tk()
root.title('display')
square_size = 50

path = result[1]

for row in range(5):
    for col in range(5):

        reward_value = reward_table[row][col]
        match reward_value:
            case 100:
                colour = "green"
            case -999:
                colour = "red"
            case -20:
                colour = "blue"
            case _:
                colour = "lightgray"
        if (row, col) in path:
            colour = "yellow"

        square = tk.Label(root, width=square_size//10, height=square_size//15, bg=colour, borderwidth=1, relief="solid")
        square.grid(row=row, column=col, padx=1, pady=1)

root.mainloop()
