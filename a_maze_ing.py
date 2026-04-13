import sys
import os
import mazegen.generator as gen
from config_parser import parse_config
from mazegen.generator import MazeGenerator
from typing import Dict, Any, List, Tuple


def show_welcome() -> None:
    """Display a beautiful welcome screen before the maze starts."""
    import time
    import re

    Yellow_Green = "\x1b[38;5;154m"
    BOLD = "\x1b[38;5;154m"
    RESET = "\x1b[38;5;154m"

    def visible_len(s: str) -> int:
        ansi_escape = re.compile(r'\033\[[0-9;]*m')
        return len(ansi_escape.sub('', s))

    def box_line(content: str, width: int = 54) -> str:
        padding = width - visible_len(content)
        return (
            Yellow_Green + "║ " + RESET +
            content + " " * padding +
            Yellow_Green + " ║" + RESET
        )

    os.system("clear")

    W = 54

    print(Yellow_Green + "╔" + "═" * (W + 2) + "╗" + RESET)

    # content of the welcome msg ---------------------------------------
    content_lines = [
        Yellow_Green + "░" * W + RESET,
        "",
        BOLD + Yellow_Green + " ███╗   ███╗ █████╗ ███████╗███████╗" + RESET,
        BOLD + Yellow_Green + " ████╗ ████║██╔══██╗╚══███╔╝██╔════╝" + RESET,
        BOLD + Yellow_Green + " ██╔████╔██║███████║  ███╔╝ █████╗  " + RESET,
        BOLD + Yellow_Green + " ██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝  " + RESET,
        BOLD + Yellow_Green + " ██║ ╚═╝ ██║██║  ██║███████╗███████╗" + RESET,
        BOLD + Yellow_Green + " ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝" + RESET,
        "",
        Yellow_Green + "░" * W + RESET,
        "",
        (BOLD + Yellow_Green
         + "  ✦ ✦  M A Z E   G E N E R A T O R  ✦ ✦  "
         + RESET
         ),
        "",
        (Yellow_Green
         + "  Algorithms " + RESET + "│"
         + Yellow_Green + " DFS  ·  Prim                    " + RESET
         ),
        (Yellow_Green
         + "  Features   " + RESET + "│"
         + Yellow_Green + " Animation · Perfect · 42        " + RESET
         ),
        (Yellow_Green
         + "  Version    " + RESET + "│"
         + Yellow_Green + " v1.0.0                          " + RESET
         ),
        "",
        Yellow_Green + '  "A labyrinth is not a place to be lost,  ' + RESET,
        Yellow_Green + '     but a path to be found." — Anonymous  ' + RESET,
        "",
    ]

    # ptint content bar --------------------------------------------------
    for line in content_lines:
        print(box_line(line, W))
        time.sleep(0.04)

    # Loading bar --------------------------------------------------------
    BAR_WIDTH = 24
    bar_prefix = "  Loading  "
    bar_suffix = "  " + BOLD + Yellow_Green + "Ready ✓" + RESET

    print(Yellow_Green + "║ " + RESET + bar_prefix, end="", flush=True)
    for _ in range(BAR_WIDTH):
        time.sleep(0.05)
        print(Yellow_Green + "█" + RESET, end="", flush=True)

    suffix_padding = W - len(bar_prefix) - BAR_WIDTH - visible_len(bar_suffix)
    print(bar_suffix + " " * suffix_padding + Yellow_Green + " ║" + RESET)

    # Enter prompt --------------------------------------------------------
    print(box_line("", W))
    enter_msg = (Yellow_Green + "    Press " + BOLD
                 + Yellow_Green + "[ ENTER ]" + RESET
                 + Yellow_Green + " to enter the maze...    " + RESET)
    print(box_line(enter_msg, W))

    print(Yellow_Green + "╚" + "═" * (W + 2) + "╝" + RESET)

    input()


def show_goodbye() -> None:
    """Display a beautiful goodbye screen at the end of the program."""
    import time
    import re

    Yellow_Green = "\x1b[38;5;154m"
    BOLD = "\x1b[38;5;154m"
    RESET = "\x1b[38;5;154m"

    def visible_len(s: str) -> int:
        """Return visible length ignoring ANSI codes."""
        ansi_escape = re.compile(r'\033\[[0-9;]*m')
        return len(ansi_escape.sub('', s))

    def box_line(content: str, width: int = 54) -> str:
        """Return a bordered line padded to exact width."""
        padding = width - visible_len(content)
        return (Yellow_Green + "║ " + RESET + content
                + " " * padding + Yellow_Green + " ║" + RESET)

    os.system("clear")

    W = 54

    print(Yellow_Green + "╔" + "═" * (W + 2) + "╗" + RESET)

    content_lines = [
        Yellow_Green + "░" * W + RESET,
        "",
        BOLD + Yellow_Green + "  ██████╗ ██╗   ██╗███████╗       " + RESET,
        BOLD + Yellow_Green + " ██╔══██╗╚██╗ ██╔╝██╔════╝       " + RESET,
        BOLD + Yellow_Green + " ██████╔╝ ╚████╔╝ █████╗         " + RESET,
        BOLD + Yellow_Green + " ██╔══██╗  ╚██╔╝  ██╔══╝         " + RESET,
        BOLD + Yellow_Green + " ██████╔╝   ██║   ███████╗        " + RESET,
        BOLD + Yellow_Green + " ╚═════╝    ╚═╝   ╚══════╝        " + RESET,
        "",
        Yellow_Green + "░" * W + RESET,
        "",
        (BOLD + Yellow_Green
         + "  ✦ ✦  Thanks for playing A-Maze-ing  ✦ ✦  " + RESET),
        "",
        (Yellow_Green + "  Mazes solved   " + RESET
         + "│" + Yellow_Green + " Hope you found your path!      " + RESET
         ),
        (Yellow_Green + "  Come back      " + RESET +
         "│" + Yellow_Green + " New mazes await you            " + RESET),
        (Yellow_Green + "  Version        " + RESET
         + "│" + Yellow_Green + " v1.0.0                         " + RESET),
        "",
        Yellow_Green + '  "A labyrinth is not a place to be lost,  ' + RESET,
        Yellow_Green + '     but a path to be found." — Anonymous  ' + RESET,
        "",
    ]

    for line in content_lines:
        print(box_line(line, W))
        time.sleep(0.04)

    # --- Goodbye bar -----------------------------------------------------
    BAR_WIDTH = 24
    bar_prefix = "  Closing  "
    bar_suffix = "  " + BOLD + Yellow_Green + "Goodbye ✓" + RESET

    print(Yellow_Green + "║ " + RESET + bar_prefix, end="", flush=True)
    for _ in range(BAR_WIDTH):
        time.sleep(0.05)
        print(Yellow_Green + "█" + RESET, end="", flush=True)

    suffix_padding = W - len(bar_prefix) - BAR_WIDTH - visible_len(bar_suffix)
    print(bar_suffix + " " * suffix_padding + Yellow_Green + " ║" + RESET)

    print(box_line("", W))
    print(Yellow_Green + "╚" + "═" * (W + 2) + "╝" + RESET)


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
        ("\033[34m", "Yellow_Green"),
        ("\033[31m", "Red"),
        ("\033[32m", "Yellow_Green"),
        ("\033[33m", "Yellow"),
        ("\033[35m", "Yellow_Green"),
        ("\x1b[46m", "Yellow_Green BG"),
        ("\x1b[38;5;154m", "Yellow Yellow_Green"),
        ("\033[93m", "Light Yellow"),
        ("\x1b[38;5;31m", "Steel Yellow_Green"),
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

    write_output(maze, path, path_string, maze_config["OUTPUT_FILE"])

    while True:
        os.system("clear")

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
            show_goodbye()
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
