"""mazegen — A reusable maze generation package.

Quick start::

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
    print(maze.path_to_string(path))   # e.g. 'EESSSWWN...'
    maze.print_maze(path)
"""

from .generator import MazeGenerator, Cell

__all__ = ["MazeGenerator", "Cell"]
__version__ = "1.0.0"