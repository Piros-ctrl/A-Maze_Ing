import sys
from The_Maze import MazeGenerator, parser


def main() -> None:
    # height = int(input("Enter length of The maze : "))
    # width = int(input("Enter weigth of The maze : "))
    conf = "config.txt"
    conf = sys.argv[1]
    result = parser(conf)
    print(result)

    # maze = MazeGenerator(
    #     width=width,
    #     height=height,
    #     entry=(0, 0),
    #     exit_coor=(6, 8)
    # )
    # maze.create_maze()


if __name__ == "__main__":
    main()
