import random

N = 1
E = 2
S = 4
W = 8

OPOSITE = {
    N: S,
    E: W,
    S: N,
    W: E
}

DIRECTIONS = [
    (-1, 0, N),
    (0, 1, E),
    (1, 0, S),
    (0, -1, W)
]


def break_wall(current, nighbor, direction):
    current.walls &= ~direction
    nighbor.walls &= ~OPOSITE[direction]


def dfs(maze, row, col, hight, width):
    if maze[row][col].pattern:
        print("Cannot start from inside The 42 pattern")
        exit(0)
    maze[row][col].visited = True

    suflled_directions = DIRECTIONS[:]
    random.shuffle(suflled_directions)

    for dr, dc, direction in suflled_directions:
        new_row = row + dr
        new_col = col + dc

        if new_row < 0 or new_row >= hight:
            continue
        if new_col < 0 or new_col >= width:
            continue
        if maze[new_row][new_col].visited:
            continue
        if maze[new_row][new_col].pattern:
            continue

        break_wall(maze[row][col], maze[new_row][new_col], direction)
        dfs(maze, new_row, new_col, hight, width)
