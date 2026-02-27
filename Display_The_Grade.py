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
            Cell = maze[r][c]
            vertical += "   "
            if Cell.Walls["Bottom"]:
                vertical += "|"
            else:
                vertical += " "
            if Cell.Walls["Right"]:
                horizontal += "---o"
            else:
                horizontal += "   "
        print(vertical)
        print(horizontal)


def creat_maze(raws, cols):
    Grid = []
    for _ in range(raws):
        raw = []
        for _ in range(cols):
            raw.append(Cell())
        Grid.append(raw)
    print_maze(Grid, raws, cols)


creat_maze(4, 4)
