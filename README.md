# A-Maze-ing 🏰

A Python maze generator using **DFS** (generation) and **BFS** (solving).

---

## Usage

```bash
python3 a_maze_ing.py config.txt
```

### Controls

| Key | Action |
|-----|--------|
| `R` | Re-generate a new maze |
| `P` | Show / Hide solution path |
| `C` | Cycle wall colours |
| `Q` | Quit |

---

## Configuration file (`config.txt`)

```ini
# Maze dimensions
WIDTH=20
HEIGHT=15

# Entry and Exit: row,col (must be on the border)
ENTRY=0,0
EXIT=14,19

# Output file
OUTPUT_FILE=maze.txt

# Perfect maze (one unique path between any two cells)
PERFECT=True

# Optional seed for reproducibility
SEED=42
```

---

## Output file format

Each cell is one hexadecimal digit encoding its closed walls:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

Example: `A` = `1010` = East and West walls closed.

After an empty line, the file contains:
1. Entry coordinates
2. Exit coordinates
3. Shortest path as a string of `N`/`E`/`S`/`W`

---

## mazegen — reusable package

### Install

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic example

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(14, 19),
    perfect=True,
    seed=42,
)
maze.create_maze()
path = maze.solve_maze()
print(maze.path_to_string(path))  # e.g. 'EESSSWWN...'
maze.print_maze(path)
```

### Custom parameters

```python
# Without seed (random each time)
maze = MazeGenerator(width=30, height=20, entry=(0,0), exit=(19,29))

# Non-perfect maze (multiple paths allowed)
maze = MazeGenerator(width=20, height=15, entry=(0,0), exit=(14,19), perfect=False)
```

### Accessing the maze structure

```python
maze.create_maze()

# 2D grid of Cell objects
cell = maze.grid[row][col]
print(cell.walls)    # int bitmask: N=1, E=2, S=4, W=8
print(cell.pattern)  # True if part of '42' decoration

# Solve and get path
path = maze.solve_maze()              # list of (row, col) tuples
directions = maze.path_to_string(path)  # 'EESSSWWN...'
```

---

## Build the package from source

```bash
cd mazegen/
pip install build
python3 -m build
# produces: dist/mazegen-1.0.0-py3-none-any.whl
```

---

## Makefile

```bash
make install      # install dependencies
make run          # run the maze
make debug        # run with pdb debugger
make clean        # remove cache files
make lint         # flake8 + mypy
make lint-strict  # flake8 + mypy --strict
make package      # build the mazegen pip package
```