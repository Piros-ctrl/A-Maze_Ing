import The_pattern
import Generate_Maze_Path

class Cell:
    def __init__(self):
        self.Walls = {
            "Top": True,
            "Bottom": True,
            "Left": True,
            "Right": True
        }


def print_maze(maze, rows, cols, path):
    print("o" + "---o" * cols)
    for r in range(rows):
        vertical = "|"
        horizontal = "o"
        for c in range(cols):
            cell = maze[r][c]

            if (r,c) in path:
                vertical += " x "
            else:
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


def creat_maze(rows, cols):
    Grid = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(Cell())
        Grid.append(row)
        exit = (rows-1, cols-1)
    Generate_Maze_Path.generat_path(Grid, exit, rows, cols)
    if rows >= 7 and cols >= 9:
        The_pattern.pattern_42(Grid, rows, cols)
        print_maze(Grid, rows, cols)
    else:
        print("The Demention that you put is to small for The MAZE")

def main():
    rows = int(input("Enter length of The maze : "))
    cols = int(input("Enter weigth of The maze : "))
    creat_maze(rows, cols)


main()
