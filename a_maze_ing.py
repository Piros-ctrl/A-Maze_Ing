import sys
from config_parser import parse_config
from generator import MazeGenerator, WALL
from typing import Dict

def interactive_mode(maze_config: Dict) -> None:
    show_path = True
    wall_colors = [
        ("\033[34m", "Blue"),
        ("\033[31m", "Red"),
        ("\033[32m", "Green"),
        ("\033[33m", "Yellow"),
    ]
    color_index = 0

    def generate_new():
        maze = MazeGenerator(
            width=maze_config["WIDTH"],
            height=maze_config["HEIGHT"],
            entry=maze_config["ENTRY"],
            exit=maze_config["EXIT"],
            perfect=maze_config["PERFECT"],
            seed=maze_config.get("SEED")
        )
        maze.create_maze()
        return maze

    maze = generate_new()
    path = maze.solve_maze()

    while True:
        print("\033[H\033[J", end="")
        maze.print_maze(path if show_path else [])

        print("\n--- Controls ---")
        print("[R] Re-generate maze")
        print("[P] Show/Hide path")
        print("[C] Change wall color")
        print("[Q] Quit")

        choice = input("\nYour choice: ").strip().upper()

        if choice == "R":
            maze = generate_new()
            path = maze.solve_maze()
        elif choice == "P":
            show_path = not show_path
        elif choice == "C":
            color_index = (color_index + 1) % len(wall_colors)
            color, name = wall_colors[color_index]
            import generator
            generator.WALL = color + "█" + "\033[0m"
        elif choice == "Q":
            print("Goodbye!")
            break

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    config_file = sys.argv[1]

    try:
        config = parse_config(config_file)

        if config["WIDTH"] < 7 or config["HEIGHT"] < 5:
            print("Warning: Maze too small to include '42' pattern")

        interactive_mode(config)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()