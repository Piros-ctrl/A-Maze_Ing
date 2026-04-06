from Generate_Maze_Path import generate_path, path_to_directions
from The_pattern import pattern_42
from D_F_S import dfs, N, E, S, W


class Cell:
    def __init__(self):
        self.walls = N | E | S | W
        self.visited = False
        self.pattern = False


def print_maze(maze, rows, cols, path):
    height = rows * 2 + 1
    width = cols * 4 + 1

    canvas = []
    for _ in range(height):
        canvas.append([" "] * width)

    for r in range(rows):
        for c in range(cols):
            cell = maze[r][c]

            y = r * 2
            x = c * 4

            canvas[y][x] = "█"
            canvas[y][x + 4] = "█"
            canvas[y + 2][x] = "█"
            canvas[y + 2][x + 4] = "█"

            if cell.walls & N:
                canvas[y][x + 1] = "█"
                canvas[y][x + 2] = "█"
                canvas[y][x + 3] = "█"

            if cell.walls & S:
                canvas[y + 2][x + 1] = "█"
                canvas[y + 2][x + 2] = "█"
                canvas[y + 2][x + 3] = "█"

            if cell.walls & W:
                canvas[y + 1][x] = "█"

            if cell.walls & E:
                canvas[y + 1][x + 4] = "█"

    for line in canvas:
        print("".join(line))


def creat_maze(hight, width):
    grid = []
    for _ in range(hight):
        row = []
        for _ in range(width):
            row.append(Cell())
        grid.append(row)
    pattern_42(grid, hight, width)
    dfs(grid, 0, 0, hight, width)
    start = (0, 0)
    exit = (6, 8)
    path = generate_path(grid, hight, width, start, exit)
    path_direction = path_to_directions(path)
    print_maze(grid, hight, width, path)
    print()
    print(path_direction)


def main():
    hight = int(input("Enter length of The maze : "))
    # rows = 7
    width = int(input("Enter weigth of The maze : "))
    # cols = 9
    creat_maze(hight, width)


main()
