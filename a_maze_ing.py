from The_Maze import MazeGenerator


def main() -> None:
    height = int(input("Enter length of The maze : "))
    width = int(input("Enter weigth of The maze : "))

    maze = MazeGenerator(
        width=width,
        height=height,
        entry=(0, 0),
        exit_coor=(6, 8)
    )
    maze.create_maze()


if __name__ == "__main__":
    main()
    