from D_F_S import N, E, S, W


def switch_cells_to_false(grid, rows, cols):
    for r in range(rows):
        for c in range(cols):
            if grid[r][c].pattern:
                continue
            grid[r][c].visited = False


def build_path(parent, start, end):
    path = []
    current = end

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()
    return path


def path_to_directions(path):
    directions = ""

    for i in range(1, len(path)):
        prev_x, prev_y = path[i - 1]
        curr_x, curr_y = path[i]

        if curr_x == prev_x - 1 and curr_y == prev_y:
            directions += "N"
        elif curr_x == prev_x and curr_y == prev_y + 1:
            directions += "E"
        elif curr_x == prev_x + 1 and curr_y == prev_y:
            directions += "S"
        elif curr_x == prev_x and curr_y == prev_y - 1:
            directions += "W"

    return directions


def generate_path(grid, rows, cols, start, end):
    switch_cells_to_false(grid, rows, cols)

    queue = [start]
    parent = {}
    while queue:
        x, y = queue.pop(0)
        cell = grid[x][y]

        cell.visited = True

        if (x, y) == end:
            return build_path(parent, start, end)

        if not (cell.walls & N):
            if not grid[x - 1][y].visited:
                if (x - 1, y) not in parent and (x - 1, y) != start:
                    parent[(x - 1, y)] = (x, y)
                queue.append((x - 1, y))

        if not (cell.walls & E):
            if not grid[x][y + 1].visited:
                if (x, y + 1) not in parent and (x, y + 1) != start:
                    parent[(x, y + 1)] = (x, y)
                queue.append((x, y + 1))

        if not (cell.walls & S):
            if not grid[x + 1][y].visited:
                if (x + 1, y) not in parent and (x + 1, y) != start:
                    parent[(x + 1, y)] = (x, y)
                queue.append((x + 1, y))

        if not (cell.walls & W):
            if not grid[x][y - 1].visited:
                if (x, y - 1) not in parent and (x, y - 1) != start:
                    parent[(x, y - 1)] = (x, y)
                queue.append((x, y - 1))

    return None