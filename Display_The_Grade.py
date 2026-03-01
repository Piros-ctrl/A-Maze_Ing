import The_pattern

class Cell:
    def __init__(self):
        self.Walls = {
            "Top": True,
            "Bottom": True,
            "Left": True,
            "Right": True
        }


def print_maze(maze, raws, cols):
    print("o" + "---o" * cols)
    for r in range(raws):
        vertical = "|"
        horizontal = "o"
        for c in range(cols):
            cell = maze[r][c]

            vertical += "   "
            if cell.Walls["Right"]:
                vertical += "|"
            else:
                vertical += " "

            if cell.Walls["Bottom"]:
                horizontal += "---o"
            else:
                horizontal += "   o"

        print(vertical)
        print(horizontal)


def creat_maze(raws, cols):
    Grid = []
    for _ in range(raws):
        row = []
        for _ in range(cols):
            row.append(Cell())
        Grid.append(row)
    if raws >= 7 and cols >= 9:
        The_pattern.pattern_42(Grid, raws, cols)
        print_maze(Grid, raws, cols)
    else:
        print("The Demention that you put is to small for The MAZE")

def main():
    rows = int(input("Enter length of The maze : "))
    cols = int(input("Enter weigth of The maze : "))
    creat_maze(rows, cols)


main()
