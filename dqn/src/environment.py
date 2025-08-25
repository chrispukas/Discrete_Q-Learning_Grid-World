
class tile:
    weighted_value = 0
    move_value = 0

    def __init__(self, Weighted_value, Move_value):
        self.weighted_value = Weighted_value
        self.move_value = Move_value


def create_reward_table():
    reward_table = [[100, -1, -1, -1, -1],
                    [-1, -99, -99, -1, -1],
                    [-1, -99, -99, -1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -20],]
    # values:
    # ■ 'Solid' tile: -30
    # □ 'Empty' tile: -1
    # G 'Goal' tile: +100
    # S 'Start' tile: -20 (unfavourable to go back to beginning)
    # =====================
    # G □ □ □ □
    # □ ■ ■ □ □
    # □ ■ ■ □ □
    # □ □ □ □ □
    # □ □ □ □ S
    # =====================

    return reward_table

def print_env(env):
    for row in env:
        print('\n')
        for cell in row:
            print(interpret_cell_value(cell), end=" ")

def interpret_cell_value(value):
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