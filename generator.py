import random
from typing import List, Tuple

# Directions
N = 1
E = 2
S = 4
W = 8

OPPOSITE = {
    N: S,
    E: W,
    S: N,
    W: E
}

# Colors & symbols
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"

WALL = BLUE + "█" + RESET
PATTERN = RED + "█" + RESET
PATH = "⚽️"
EMPTY = " "


class Cell:
    def __init__(self) -> None:
        self.walls = N | E | S | W
        self.visited = False
        self.pattern = False


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool = True,
        seed: int = None
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        if seed is not None:
            random.seed(seed)
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.directions = [
            (-1, 0, N),
            (0, 1, E),
            (1, 0, S),
            (0, -1, W)
        ]

    def break_wall(
            self,
            current: Cell,
            neighbor: Cell,
            direction: int
            ) -> None:
        current.walls &= ~direction
        neighbor.walls &= ~OPPOSITE[direction]

    def _unvisited_cells(
                self,
                current_cell: Tuple[int, int]
                ) -> List[Tuple[int, int, int]]:
            neighbors = []
            row, col = current_cell

            for dr, dc, direction in self.directions:
                new_row = row + dr
                new_col = col + dc
                if (
                    0 <= new_row < self.height and
                    0 <= new_col < self.width
                ):
                    if self.grid[new_row][new_col].pattern:
                        continue
                    if not self.grid[new_row][new_col].visited:
                        neighbors.append((new_row, new_col, direction))
            return neighbors

    def run_dfs(self) -> None:
            stack: List[Tuple[int, int]] = []
            entry_row, entry_col = self.entry

            if self.grid[entry_row][entry_col].pattern:
                print("Cannot start from inside The 42 pattern")
                return

            self.grid[entry_row][entry_col].visited = True
            stack.append((entry_row, entry_col))

            while stack:
                current_cell = stack[-1]
                neighbors = self._unvisited_cells(current_cell)

                if neighbors:
                    chosen_neighbor = random.choice(neighbors)
                    new_row, new_col, direction = chosen_neighbor
                    current_row, current_col = current_cell

                    self.break_wall(
                        self.grid[current_row][current_col],
                        self.grid[new_row][new_col],
                        direction
                    )
                    self.grid[new_row][new_col].visited = True
                    stack.append((new_row, new_col))
                else:
                    stack.pop()


    # Symbol 42 patterns
    def draw_4(self, row: int, col: int) -> None:
        self.grid[row][col].pattern = True
        self.grid[row + 1][col].pattern = True
        self.grid[row + 2][col].pattern = True
        self.grid[row + 2][col + 1].pattern = True
        self.grid[row + 2][col + 2].pattern = True
        self.grid[row + 3][col + 2].pattern = True
        self.grid[row + 4][col + 2].pattern = True

    def draw_2(self, row: int, col: int) -> None:
        self.grid[row][col].pattern = True
        self.grid[row][col + 1].pattern = True
        self.grid[row][col + 2].pattern = True
        self.grid[row + 1][col + 2].pattern = True
        self.grid[row + 2][col + 1].pattern = True
        self.grid[row + 2][col + 2].pattern = True
        self.grid[row + 2][col].pattern = True
        self.grid[row + 3][col].pattern = True
        self.grid[row + 4][col].pattern = True
        self.grid[row + 4][col + 1].pattern = True
        self.grid[row + 4][col + 2].pattern = True

    def symbol_42(self) -> None:
        row = (self.height - 5) // 2
        col = (self.width - 7) // 2
        self.draw_4(row, col)
        self.draw_2(row, col + 4)

    # Solve maze BFS
    def switch_cells_to_false(self) -> None:
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col].pattern:
                    continue
                self.grid[row][col].visited = False

    
    def solve_maze(self) -> List[Tuple[int, int]]:
        self.switch_cells_to_false()

        queue = [self.entry]
        parent = {}
        visited = set()
        visited.add(self.entry)

        while queue:
            row, col = queue.pop(0)

            if (row, col) == self.exit:
                return self.create_path(parent, self.entry, self.exit)

            cell = self.grid[row][col]

            for dr, dc, direction in self.directions:
                new_row, new_col = row + dr, col + dc
                if (
                    0 <= new_row < self.height and
                    0 <= new_col < self.width and
                    not (cell.walls & direction) and
                    (new_row, new_col) not in visited and
                    not self.grid[new_row][new_col].pattern
                ):
                    visited.add((new_row, new_col)) 
                    parent[(new_row, new_col)] = (row, col)
                    queue.append((new_row, new_col))

        return []

    def create_path(self, parent: dict, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = []
        current = end
        while current != start:
            path.append(current)
            current = parent[current]
        path.append(start)
        path.reverse()
        return path

    def path_to_string(self, path: List[Tuple[int, int]]) -> str:
        directions = ""
        for i in range(1, len(path)):
            prev_row, prev_col = path[i - 1]
            curr_row, curr_col = path[i]
            if curr_row == prev_row - 1 and curr_col == prev_col:
                directions += "N"
            elif curr_row == prev_row and curr_col == prev_col + 1:
                directions += "E"
            elif curr_row == prev_row + 1 and curr_col == prev_col:
                directions += "S"
            elif curr_row == prev_row and curr_col == prev_col - 1:
                directions += "W"
        return directions

    def print_maze(self, path: List[Tuple[int, int]]) -> None:
        maze_height = self.height * 2 + 1
        maze_width = self.width * 4 + 1
        maze = [[" "] * maze_width for _ in range(maze_height)]
        for row in range(self.height):
            for col in range(self.width):
                cell = self.grid[row][col]
                y = row * 2
                x = col * 4
                maze[y][x] = WALL
                maze[y][x + 4] = WALL
                maze[y + 2][x] = WALL
                maze[y + 2][x + 4] = WALL
                if cell.pattern:
                    maze[y + 1][x + 1] = PATTERN
                    maze[y + 1][x + 2] = PATTERN
                    maze[y + 1][x + 3] = PATTERN
                if (row, col) in path:
                    maze[y + 1][x + 2] = PATH
                    maze[y + 1][x + 3] = ""
                if cell.walls & N:
                    maze[y][x + 1] = WALL
                    maze[y][x + 2] = WALL
                    maze[y][x + 3] = WALL
                if cell.walls & S:
                    maze[y + 2][x + 1] = WALL
                    maze[y + 2][x + 2] = WALL
                    maze[y + 2][x + 3] = WALL
                if cell.walls & W:
                    maze[y + 1][x] = WALL
                if cell.walls & E:
                    maze[y + 1][x + 4] = WALL
        for line in maze:
            print("".join(line))
    
    def open_entry_exit(self) -> None:
        entry_row, entry_col = self.entry
        exit_row, exit_col = self.exit

        if entry_col == 0:
            self.grid[entry_row][entry_col].walls &= ~W 
        elif entry_row == 0:
            self.grid[entry_row][entry_col].walls &= ~N
        elif entry_col == self.width - 1:
            self.grid[entry_row][entry_col].walls &= ~E
        elif entry_row == self.height - 1:
            self.grid[entry_row][entry_col].walls &= ~S

        if exit_col == self.width - 1:
            self.grid[exit_row][exit_col].walls &= ~E
        elif exit_row == self.height - 1:
            self.grid[exit_row][exit_col].walls &= ~S
        elif exit_col == 0:
            self.grid[exit_row][exit_col].walls &= ~W
        elif exit_row == 0:
            self.grid[exit_row][exit_col].walls &= ~N


    def create_maze(self) -> None:
        if self.height > 5 and self.width > 7:
            self.symbol_42()
        else:
            print("Error: Maze too small to include '42' pattern")

        self.run_dfs()
        # self.open_entry_exit()