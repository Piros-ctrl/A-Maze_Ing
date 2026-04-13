*This project has been created as part of the 42 curriculum by azel-mah and oabderra.*

---

# A-Maze-ing

## Description

A-Maze-ing is a maze generator and solver written in Python 3. It reads a configuration file, generates a random maze containing a **"42"** pattern, solves it using BFS, and displays everything in an interactive terminal interface.

---

## Instructions

```bash
# Install dependencies
make install

# Run the program
python3 a_maze_ing.py config.txt
```

---

## Configuration File Format

```ini
WIDTH=20          # number of columns (>9 for '42' pattern)
HEIGHT=15         # number of rows (>7 for '42' pattern)
ENTRY=0,0         # row,col — must be on the border
EXIT=14,19        # row,col — must be on the border
OUTPUT_FILE=maze.txt
PERFECT=True      # True = one unique path between any two cells
SEED=42           # optional — for reproducibility
ALGORITHM=dfs     # dfs | prim
ANIMATE=False     # True = live generation animation
```

---

## Interactive Controls

| Key | Action |
|-----|--------|
| `R` | Re-generate maze |
| `P` | Show / hide solution path |
| `C` | Change wall colour |
| `A` | Toggle animation |
| `D` | Switch to DFS |
| `M` | Switch to Prim |
| `Q` | Quit |

---

## Maze Generation Algorithm

Two algorithms are supported:

**DFS (default):** Starts from the entry, randomly carves paths using a stack, backtracks when stuck. Produces long winding corridors. Chosen for its simplicity and natural perfect maze generation.

**Prim (bonus):** Grows the maze outward from the entry by randomly picking walls from a frontier list. Produces more branching mazes with shorter dead-ends.

---

## Reusable Module — `mazegen`

The `MazeGenerator` class is packaged as a standalone pip library.

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

```python
from mazegen import MazeGenerator

maze = MazeGenerator(20, 15, (0, 0), (14, 19), seed=42)
maze.create_maze()
path = maze.solve_maze()
print(maze.path_to_string(path))  # e.g. "EESSNEEE..."
maze.print_maze(path)
```

Access the grid: `maze.grid[row][col].walls` — int bitmask (N=1, E=2, S=4, W=8)

Build from source:
```bash
pip install build && python3 -m build
```

---

## Team

Member Roles:

-Aziz: Config parser,  show_welcome ,show_goodbye, interactive mode, packaging.

-Abderrahmane: DFS/Prim algorithms, animation, output file, BFS solver.

**Planning:** We split the work by module from the start. The main challenge was the BFS bug (visited set on pop instead of push) and ANSI border alignment. Overall the project went smoothly.

**What worked well:** Clean separation between modules. **To improve:** Adding Kruskal and graphical display.

**Tools used:** Python 3, flake8, mypy, Git, VS Code, Claude (AI).

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Buckblog — Maze algorithms](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- [BFS — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python packaging guide](https://packaging.python.org/en/latest/)

**AI usage (Claude):** Used to fix the BFS bug, explain Prim's algorithm, solve ANSI border alignment, and help structure the README. All output was reviewed and tested before use.