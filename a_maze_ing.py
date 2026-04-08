import sys
from The_Maze import MazeGenerator, parser


def main() -> None:
    conf = "config.txt"
    conf = sys.argv[1]
    result = parser(conf)
    print(result)

    maze = MazeGenerator(
        width=result["WIDTH"],
        height=result["HEIGHT"],
        entry=result["ENTRY"],
        exit_coor=result["EXIT"]
    )
    maze.create_maze()


if __name__ == "__main__":
    main()
