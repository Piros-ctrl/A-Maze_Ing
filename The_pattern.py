def draw_4(Grid, r, c):
    Grid[r][c].pattern = True
    Grid[r+1][c].pattern = True
    Grid[r+2][c].pattern = True
    Grid[r+2][c+1].pattern = True
    Grid[r+2][c+2].pattern = True
    Grid[r+3][c+2].pattern = True
    Grid[r+4][c+2].pattern = True


def draw_2(Grid, r, c):
    Grid[r][c].pattern = True
    Grid[r][c+1].pattern = True
    Grid[r][c+2].pattern = True
    Grid[r+1][c+2].pattern = True
    Grid[r+2][c+1].pattern = True
    Grid[r+2][c+2].pattern = True
    Grid[r+2][c].pattern = True
    Grid[r+2][c].pattern = True
    Grid[r+3][c].pattern = True
    Grid[r+4][c].pattern = True
    Grid[r+4][c+1].pattern = True
    Grid[r+4][c+2].pattern = True


def pattern_42(Grid, hight, width):
    r = (hight - 5) // 2
    c = (width - 7) // 2
    draw_4(Grid, r, c)
    draw_2(Grid, r, c+4)
