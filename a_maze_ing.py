"""A-Maze-ing — main entry point."""

import sys
import mazegen.generator as gen
from config_parser import parse_config
from mazegen.generator import MazeGenerator
from typing import Dict, Any, List, Tuple
# ====== aziz ==========================================================
def show_welcome() -> None:
    """Display a beautiful welcome screen before the maze starts."""
    import time
    import re

    CYAN    = "\033[36m"
    YELLOW  = "\033[33m"
    MAGENTA = "\033[35m"
    GREEN   = "\033[32m"
    BLUE    = "\033[34m"
    DIM     = "\033[2m"
    BOLD    = "\033[1m"
    RESET   = "\033[0m"

    def visible_len(s: str) -> int:
        ansi_escape = re.compile(r'\033\[[0-9;]*m')
        return len(ansi_escape.sub('', s))

    def box_line(content: str, width: int = 54) -> str:
        padding = width - visible_len(content)
        return CYAN + "║ " + RESET + content + " " * padding + CYAN + " ║" + RESET

    print("\033[H\033[J", end="")

    W = 54

    print(CYAN + "╔" + "═" * (W + 2) + "╗" + RESET)

    # content of the welcome msg ---------------------------------------
    content_lines = [
        DIM + "░" * W + RESET,
        "",
        BOLD + YELLOW + " ███╗   ███╗ █████╗ ███████╗███████╗" + RESET,
        BOLD + YELLOW + " ████╗ ████║██╔══██╗╚══███╔╝██╔════╝" + RESET,
        BOLD + YELLOW + " ██╔████╔██║███████║  ███╔╝ █████╗  " + RESET,
        BOLD + YELLOW + " ██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝  " + RESET,
        BOLD + YELLOW + " ██║ ╚═╝ ██║██║  ██║███████╗███████╗" + RESET,
        BOLD + YELLOW + " ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝" + RESET,
        "",
        DIM + "░" * W + RESET,
        "",
        BOLD + MAGENTA + "  ✦ ✦  M A Z E   G E N E R A T O R  ✦ ✦  " + RESET,
        "",
        BLUE + "  Algorithms " + RESET + "│" + GREEN + " DFS  ·  Prim                    " + RESET,
        BLUE + "  Features   " + RESET + "│" + GREEN + " Animation · Perfect · 42        " + RESET,
        BLUE + "  Version    " + RESET + "│" + GREEN + " v1.0.0                          " + RESET,
        "",
        DIM + '  "A labyrinth is not a place to be lost,  ' + RESET,
        DIM + '     but a path to be found." — Anonymous  ' + RESET,
        "",
    ]

    # ptint content bar --------------------------------------------------
    for line in content_lines:
        print(box_line(line, W))
        time.sleep(0.04)

    # Loading bar --------------------------------------------------------
    BAR_WIDTH = 24
    bar_prefix = "  Loading  "
    bar_suffix = "  " + BOLD + GREEN + "Ready ✓" + RESET

    print(CYAN + "║ " + RESET + bar_prefix, end="", flush=True)
    for _ in range(BAR_WIDTH):
        time.sleep(0.05)
        print(GREEN + "█" + RESET, end="", flush=True)

    suffix_padding = W - len(bar_prefix) - BAR_WIDTH - visible_len(bar_suffix)
    print(bar_suffix + " " * suffix_padding + CYAN + " ║" + RESET)

    # Enter prompt --------------------------------------------------------
    print(box_line("", W))
    enter_msg = YELLOW + "    Press " + BOLD + MAGENTA + "[ ENTER ]" + RESET + YELLOW + " to enter the maze...    " + RESET
    print(box_line(enter_msg, W))

    print(CYAN + "╚" + "═" * (W + 2) + "╝" + RESET)

    input()
    
def write_output(
    maze: MazeGenerator,
    path: List[Tuple[int, int]],
    path_string: str,
    output_file: str,
) -> None:
    """Write the maze to an output file in hex format."""
    with open(output_file, "w") as f:
        for row in range(maze.height):
            line = ""
            for col in range(maze.width):
                line += format(maze.grid[row][col].walls, "X")
            f.write(line + "\n")
        f.write("\n")
        f.write(f"{maze.entry[0]},{maze.entry[1]}\n")
        f.write(f"{maze.exit[0]},{maze.exit[1]}\n")
        f.write(path_string + "\n")


def interactive_mode(maze_config: Dict[str, Any]) -> None:
    """Run the maze in interactive terminal mode."""
    show_path = False
    animate = False
    algorithm = "dfs"

    wall_colors = [
        ("\033[95m", "purple"),
        ("\033[34m", "Blue"),
        ("\033[31m", "Red"),
        ("\033[32m", "Green"),
        ("\033[33m", "Yellow"),
        ("\033[35m", "Magenta"),
        ("\x1b[46m", "Cyan BG"),
        ("\x1b[38;5;154m", "Yellow Green"),
        ("\033[93m","Light Yellow"), 
        ("\x1b[38;5;31m", "Steel Blue"),
        ("\x1b[38;5;247m", "Light Gray"),
        ("\x1b[38;5;206m", "Pink"),
    ]
    color_index = 0

    def generate_new() -> MazeGenerator:
        """Create and return a freshly generated maze."""
        maze = MazeGenerator(
            width=maze_config["WIDTH"],
            height=maze_config["HEIGHT"],
            entry=maze_config["ENTRY"],
            exit=maze_config["EXIT"],
            perfect=maze_config["PERFECT"],
            seed=maze_config.get("SEED"),
        )
        maze.create_maze(algorithm=algorithm, animate=animate)
        return maze

    maze = generate_new()
    path = maze.solve_maze()
    path_string = maze.path_to_string(path)

    # check is important
    if "OUTPUT_FILE" in maze_config:
        write_output(maze, path, path_string, maze_config["OUTPUT_FILE"])
        print(f"Maze saved to '{maze_config['OUTPUT_FILE']}'")

    while True:
        print("\033[H\033[J", end="")

        if maze_config["WIDTH"] <= 9 or maze_config["HEIGHT"] <= 7:
            print(
                "Warning: Maze is too small to display the '42' pattern. "
                "Use WIDTH > 9 and HEIGHT > 7."
            )
        
        maze.print_maze(path if show_path else [])

        if show_path and path:
            print(f"\nShortest path ({len(path) - 1} steps): {path_string}")
        elif not show_path:
            print("\nPath: [hidden]")
        else:
            print("\nNo path found!")

        anim_status = "ON" if animate else "OFF"
        print(f"\nAlgorithm: {algorithm.upper()} | Animation: {anim_status}")

        print("\n" + "─" * 40)
        print("[R] Re-generate maze   [P] Show/Hide path")
        print("[C] Change wall color  [A] Toggle animation")
        print("[D] DFS  [M] Prim      [Q] Quit")
        print("─" * 40)

        try:
            choice = input("Your choice: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!\n")
            break

        if choice == "R":
            maze = generate_new()
            path = maze.solve_maze()
            path_string = maze.path_to_string(path)
            if "OUTPUT_FILE" in maze_config:
                write_output(
                    maze, path, path_string, maze_config["OUTPUT_FILE"]
                )

        elif choice == "P":
            show_path = not show_path

        elif choice == "C":
            color_index = (color_index + 1) % len(wall_colors)
            color, name = wall_colors[color_index]
            gen.WALL = color + "█" + "\033[0m"
            print(f"Wall color changed to {name}.")

        elif choice == "A":
            animate = not animate
            status = "ON" if animate else "OFF"
            print(f"Animation: {status}")

        elif choice == "D":
            algorithm = "dfs"
            maze = generate_new()
            path = maze.solve_maze()
            path_string = maze.path_to_string(path)

        elif choice == "M":
            algorithm = "prim"
            maze = generate_new()
            path = maze.solve_maze()
            path_string = maze.path_to_string(path)

        elif choice == "Q":
            show_welcome()
            break

        else:
            print(f"Unknown command: '{choice}'")


def main() -> None:
    """Parse config, generate maze, and launch interactive mode."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        config = parse_config(config_file)

        show_welcome()
        interactive_mode(config)

    except (BaseException) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

