def generat_path(Grid, exit, rows, cols):
    start = (0, 0)

    Queue = [start]
    Explored = [start]
    Parent = {}

    while Queue:
        r, c = Queue.pop(0)

        if (r, c) == exit:
            break

        cell = Grid[r][c]

        if not cell.Walls["Top"] and r > 0:
            neighbor = (r - 1, c)
            if neighbor not in Explored:
                Queue.append(neighbor)
                Explored.append(neighbor)
                Parent[neighbor] = (r, c)

        if not cell.Walls["Right"] and c < cols - 1:
            neighbor = (r, c + 1)
            if neighbor not in Explored:
                Queue.append(neighbor)
                Explored.append(neighbor)
                Parent[neighbor] = (r, c)

        if not cell.Walls["Bottom"] and r < rows - 1:
            neighbor = (r + 1, c)
            if neighbor not in Explored:
                Queue.append(neighbor)
                Explored.append(neighbor)
                Parent[neighbor] = (r, c)

        if not cell.Walls["Left"] and c > 0:
            neighbor = (r, c - 1)
            if neighbor not in Explored:
                Queue.append(neighbor)
                Explored.append(neighbor)
                Parent[neighbor] = (r, c)

    path = []
    current = exit

    while current != start:
        path.append(current)
        current = Parent[current]

    path.append(start)
    path.reverse()

    return path
