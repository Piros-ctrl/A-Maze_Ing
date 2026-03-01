def draw_4(Grid, r, c):
    Grid[r][c].Walls["Bottom"] = False
    Grid[r+1][c].Walls["Bottom"] = False
    Grid[r+2][c].Walls["Right"] = False
    Grid[r+2][c+1].Walls["Right"] = False
    Grid[r+2][c+2].Walls["Bottom"] = False
    Grid[r+3][c+2].Walls["Bottom"] = False


def draw_2(Grid, r, c):
    Grid[r][c].Walls["Right"] = False
    Grid[r][c+1].Walls["Right"] = False
    Grid[r][c+2].Walls["Bottom"] = False
    Grid[r+1][c+2].Walls["Bottom"] = False
    Grid[r+2][c+1].Walls["Right"] = False
    Grid[r+2][c].Walls["Right"] = False
    Grid[r+2][c].Walls["Bottom"] = False
    Grid[r+3][c].Walls["Bottom"] = False
    Grid[r+4][c].Walls["Right"] = False
    Grid[r+4][c+1].Walls["Right"] = False


def pattern_42(Grid, row, col):
    r = (row - 5) // 2
    c = (col - 7) // 2
    draw_4(Grid, r, c)
    draw_2(Grid, r, c+4)
