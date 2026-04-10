import random
from typing import List, Optional, Tuple
# ====== abderrahmane ==========================================================
# ── Directions (bitmask) ──────────────────────────────────────────────────────
N = 1   # 0001
E = 2   # 0010
S = 4   # 0100
W = 8   # 1000

OPPOSITE: dict = {N: S, E: W, S: N, W: E}

# ── ANSI colors ───────────────────────────────────────────────────────────────
Cyan_BG = "\x1b[46m"
Light_Gray = "\x1b[38;5;247m"
Yellow_Green = "\x1b[38;5;154m"
YELLOW = "\033[33m"
RESET = "\033[0m"

WALL = Yellow_Green + "█" + RESET
PATTERN = Cyan_BG + "█" + RESET
PATH_SYMBOL = Light_Gray + "●" + RESET
ENTRY_SYMBOL = YELLOW + "E" + RESET
EXIT_SYMBOL = YELLOW + "X" + RESET


# ── Cell ──────────────────────────────────────────────────────────────────────
class Cell:
    """Represents a single cell in the maze grid."""

    def __init__(self) -> None:
        """Initialize cell with all walls closed."""
        self.walls: int = N | E | S | W
        self.visited: bool = False
        self.pattern: bool = False


# ── MazeGenerator ─────────────────────────────────────────────────────────────
class MazeGenerator:
    """Generates and solves a maze using DFS (generation) and BFS (solving)."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool = True,
        seed: Optional[int] = None,
    ) -> None:
        """Initialize and validate the maze parameters."""

        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.perfect: bool = perfect

        if seed is not None:
            random.seed(seed)

        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(width)] for _ in range(height)
        ]

        # (dr, dc, direction_bitmask)
        self.directions: List[Tuple[int, int, int]] = [
            (-1, 0, N),
            (0, 1, E),
            (1, 0, S),
            (0, -1, W),
        ]

    # ── Wall helpers ──────────────────────────────────────────────────────────
    def break_wall(
        self,
        current: Cell,
        neighbor: Cell,
        direction: int,
    ) -> None:
        """Remove the wall between two adjacent cells."""
        current.walls &= ~direction
        neighbor.walls &= ~OPPOSITE[direction]

    def _unvisited_neighbors(
        self,
        current_cell: Tuple[int, int],
    ) -> List[Tuple[int, int, int]]:
        """Return all unvisited, non-pattern neighbors of a cell."""
        neighbors: List[Tuple[int, int, int]] = []
        row, col = current_cell

        for dr, dc, direction in self.directions:
            new_row = row + dr
            new_col = col + dc
            if (
                0 <= new_row < self.height
                and 0 <= new_col < self.width
                and not self.grid[new_row][new_col].pattern
                and not self.grid[new_row][new_col].visited
            ):
                neighbors.append((new_row, new_col, direction))

        return neighbors

    # ── DFS maze generation ───────────────────────────────────────────────────
    def run_dfs(self, animate: bool = False) -> None:
        """Generate the maze using iterative DFS."""
        stack: List[Tuple[int, int]] = []
        entry_row, entry_col = self.entry
    
        if self.grid[entry_row][entry_col].pattern:
            raise ValueError("ENTRY cell is inside the '42' pattern.")
    
        self.grid[entry_row][entry_col].visited = True
        stack.append((entry_row, entry_col))
    
        while stack:
            current_cell = stack[-1]
            neighbors = self._unvisited_neighbors(current_cell)
    
            if animate:
                self._draw_frame(current_cell)
    
            if neighbors:
                chosen = random.choice(neighbors)
                new_row, new_col, direction = chosen
                current_row, current_col = current_cell
                self.break_wall(
                    self.grid[current_row][current_col],
                    self.grid[new_row][new_col],
                    direction,
                )
                self.grid[new_row][new_col].visited = True
                stack.append((new_row, new_col))
            else:
                stack.pop()

    # ── 42 pattern ────────────────────────────────────────────────────────────
    def draw_4(self, row: int, col: int) -> None:
        """Draw the digit '4' starting at (row, col). Needs 5 rows x 3 cols."""
        self.grid[row][col].pattern = True
        self.grid[row + 1][col].pattern = True
        self.grid[row + 2][col].pattern = True
        self.grid[row + 2][col + 1].pattern = True
        self.grid[row + 2][col + 2].pattern = True
        self.grid[row + 3][col + 2].pattern = True
        self.grid[row + 4][col + 2].pattern = True

    def draw_2(self, row: int, col: int) -> None:
        """Draw the digit '2' starting at (row, col). Needs 5 rows x 3 cols."""
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
        """Draw the '42' pattern in the center of the maze."""
        row = (self.height - 5) // 2
        col = (self.width - 7) // 2
        self.draw_4(row, col)
        self.draw_2(row, col + 4)

    # ── BFS solver ────────────────────────────────────────────────────────────
    def _reset_visited(self) -> None:
        """Reset the visited flag on all non-pattern cells."""
        for row in range(self.height):
            for col in range(self.width):
                if not self.grid[row][col].pattern:
                    self.grid[row][col].visited = False

    def solve_maze(self) -> List[Tuple[int, int]]:
        """Find the shortest path from entry to exit using BFS."""
        self._reset_visited()

        queue: List[Tuple[int, int]] = [self.entry]
        parent: dict = {}
        visited: set = set()
        visited.add(self.entry)

        while queue:
            row, col = queue.pop(0)

            if (row, col) == self.exit:
                return self._rebuild_path(parent, self.entry, self.exit)

            cell = self.grid[row][col]

            for dr, dc, direction in self.directions:
                new_row = row + dr
                new_col = col + dc

                if (
                    0 <= new_row < self.height
                    and 0 <= new_col < self.width
                    and not (cell.walls & direction)
                    and (new_row, new_col) not in visited
                    and not self.grid[new_row][new_col].pattern
                ):
                    visited.add((new_row, new_col))
                    parent[(new_row, new_col)] = (row, col)
                    queue.append((new_row, new_col))

        return []

    def _rebuild_path(
        self,
        parent: dict,
        start: Tuple[int, int],
        end: Tuple[int, int],
    ) -> List[Tuple[int, int]]:
        """Reconstruct the path from BFS parent map."""
        path: List[Tuple[int, int]] = []
        current = end
        while current != start:
            path.append(current)
            if current not in parent:
                return []
            current = parent[current]
        path.append(start)
        path.reverse()
        return path

    def path_to_string(self, path: List[Tuple[int, int]]) -> str:
        """Convert a path (list of cells) to a string of directions."""
        directions = ""
        for i in range(1, len(path)):
            prev_row, prev_col = path[i - 1]
            curr_row, curr_col = path[i]
            if curr_row == prev_row - 1:
                directions += "N"
            elif curr_col == prev_col + 1:
                directions += "E"
            elif curr_row == prev_row + 1:
                directions += "S"
            elif curr_col == prev_col - 1:
                directions += "W"
        return directions

    # ── Perfect maze check ────────────────────────────────────────────────────
    # ====== aziz ==========================================================
    def is_perfect(self) -> bool:
        """Check whether the maze is perfect (one unique path between any two cells).

        A perfect maze is equivalent to a spanning tree:
        all non-pattern cells are reachable from entry,
        and there are no loops.

        Returns:
            True if the maze is perfect, False otherwise.
        """
        self._reset_visited()

        # Count normal (non-pattern) cells
        normal_cells = sum(
            1
            for r in range(self.height)
            for c in range(self.width)
            if not self.grid[r][c].pattern
        )

        # BFS from entry
        visited: set = set()
        queue = [self.entry]
        visited.add(self.entry)

        while queue:
            row, col = queue.pop(0)
            cell = self.grid[row][col]

            for dr, dc, direction in self.directions:
                new_row = row + dr
                new_col = col + dc
                if (
                    0 <= new_row < self.height
                    and 0 <= new_col < self.width
                    and not (cell.walls & direction)
                    and (new_row, new_col) not in visited
                    and not self.grid[new_row][new_col].pattern
                ):
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col))

        return len(visited) == normal_cells

    # ── Open areas fix ────────────────────────────────────────────────────────
    def _is_open_3x3(self, row: int, col: int) -> bool:
        """Check if a 3x3 block starting at (row, col) is fully open.

        Args:
            row : top-left row
            col : top-left column

        Returns:
            True if the area has no internal walls (fully open 3x3), else False.
        """
        for r in range(row, row + 3):
            for c in range(col, col + 3):
                if self.grid[r][c].pattern:
                    return False
                # Check east wall (except last column of block)
                if c < col + 2 and (self.grid[r][c].walls & E):
                    return False
                # Check south wall (except last row of block)
                if r < row + 2 and (self.grid[r][c].walls & S):
                    return False
        return True

    def fix_open_areas(self) -> None:
        """Add walls to prevent open areas larger than 2x2.

        Scans every possible 3x3 block and adds a south wall
        in the center if the block is fully open.
        """
        for row in range(self.height - 2):
            for col in range(self.width - 2):
                if self._is_open_3x3(row, col):
                    # Add wall between center row and the one below it
                    self.grid[row + 1][col + 1].walls |= S
                    self.grid[row + 2][col + 1].walls |= N

    # ── ASCII display ─────────────────────────────────────────────────────────
    # ====== abderrahmane =========================================================
    def print_maze(self, path: List[Tuple[int, int]]) -> None:
        """Print the maze to the terminal using ASCII/Unicode characters."""
        path_set = set(path)
        maze_h = self.height * 2 + 1
        maze_w = self.width * 4 + 1
        display: List[List[str]] = [[" "] * maze_w for _ in range(maze_h)]

        for row in range(self.height):
            for col in range(self.width):
                cell = self.grid[row][col]
                y = row * 2
                x = col * 4

                # Corner posts
                display[y][x] = WALL
                display[y][x + 4] = WALL
                display[y + 2][x] = WALL
                display[y + 2][x + 4] = WALL

                # Pattern cells
                if cell.pattern:
                    display[y + 1][x + 1] = PATTERN
                    display[y + 1][x + 2] = PATTERN
                    display[y + 1][x + 3] = PATTERN

                # Entry / Exit markers
                if (row, col) == self.entry:
                    display[y + 1][x + 2] = ENTRY_SYMBOL
                elif (row, col) == self.exit:
                    display[y + 1][x + 2] = EXIT_SYMBOL
                # Solution path
                elif (row, col) in path_set and not cell.pattern:
                    display[y + 1][x + 2] = PATH_SYMBOL

                # Walls
                if cell.walls & N:
                    display[y][x + 1] = WALL
                    display[y][x + 2] = WALL
                    display[y][x + 3] = WALL
                if cell.walls & S:
                    display[y + 2][x + 1] = WALL
                    display[y + 2][x + 2] = WALL
                    display[y + 2][x + 3] = WALL
                if cell.walls & W:
                    display[y + 1][x] = WALL
                if cell.walls & E:
                    display[y + 1][x + 4] = WALL

        for line in display:
            print("".join(line))

    # ── Main entry point ──────────────────────────────────────────────────────
    # ====== aziz ==========================================================
    def create_maze(
        self,
        algorithm: str = "dfs",
        animate: bool = False,
    ) -> None:
        """Generate the full maze."""
        if self.height > 7 and self.width > 9:
            self.symbol_42()

        if algorithm == "prim":
            self.run_prims(animate=animate)
        else:
            self.run_dfs(animate=animate)
    
        self.fix_open_areas()
    
        if self.perfect and not self.is_perfect():
            raise ValueError(
                "Generated maze is not perfect. Try a different seed."
            )
    

    # ====== abderrahmane ==========================================================
    def _draw_frame(
        self,
        current: Tuple[int, int],
    ) -> None:
        """Print one animation frame with the current cell highlighted."""
        import sys
        import time

        maze_h = self.height * 2 + 1
        maze_w = self.width * 4 + 1
        display: List[List[str]] = [
            [" "] * maze_w for _ in range(maze_h)
        ]

        for row in range(self.height):
            for col in range(self.width):
                cell = self.grid[row][col]
                y = row * 2
                x = col * 4

                # Corner posts
                display[y][x] = WALL
                display[y][x + 4] = WALL
                display[y + 2][x] = WALL
                display[y + 2][x + 4] = WALL

                # Pattern cells
                if cell.pattern:
                    display[y + 1][x + 1] = PATTERN
                    display[y + 1][x + 2] = PATTERN
                    display[y + 1][x + 3] = PATTERN

                # Current cell = magenta dot
                if (row, col) == current:
                    display[y + 1][x + 2] = "\033[35m●\033[0m"
                elif (row, col) == self.entry:
                    display[y + 1][x + 2] = ENTRY_SYMBOL
                elif (row, col) == self.exit:
                    display[y + 1][x + 2] = EXIT_SYMBOL

                # Walls
                if cell.walls & N:
                    display[y][x + 1] = WALL
                    display[y][x + 2] = WALL
                    display[y][x + 3] = WALL
                if cell.walls & S:
                    display[y + 2][x + 1] = WALL
                    display[y + 2][x + 2] = WALL
                    display[y + 2][x + 3] = WALL
                if cell.walls & W:
                    display[y + 1][x] = WALL
                if cell.walls & E:
                    display[y + 1][x + 4] = WALL

        # Clear screen then print new frame
        sys.stdout.write("\033[H\033[J")
        for line in display:
            sys.stdout.write("".join(line) + "\n")
        sys.stdout.write(" Generating maze...\n")
        sys.stdout.flush()
        time.sleep(0.03)
    # --------------------------------------------------

    def run_prims(self, animate: bool = False) -> None:
        """Generate maze using Randomised Prim's algorithm."""
        start_row, start_col = self.entry
        self.grid[start_row][start_col].visited = True

        frontier: List[Tuple[int, int, int, int, int]] = []

        for dr, dc, direction in self.directions:
            nr, nc = start_row + dr, start_col + dc
            if (
                0 <= nr < self.height
                and 0 <= nc < self.width
                and not self.grid[nr][nc].visited
                and not self.grid[nr][nc].pattern
            ):
                frontier.append((start_row, start_col, nr, nc, direction))

        while frontier:
            idx = random.randrange(len(frontier))
            fr, fc, nr, nc, direction = frontier[idx]
            frontier.pop(idx)

            if self.grid[nr][nc].visited:
                continue

            self.break_wall(
                self.grid[fr][fc],
                self.grid[nr][nc],
                direction,
            )
            self.grid[nr][nc].visited = True

            if animate:
                self._draw_frame((nr, nc))

            for dr, dc, d in self.directions:
                nnr, nnc = nr + dr, nc + dc
                if (
                    0 <= nnr < self.height
                    and 0 <= nnc < self.width
                    and not self.grid[nnr][nnc].visited
                    and not self.grid[nnr][nnc].pattern
                ):
                    frontier.append((nr, nc, nnr, nnc, d))
