"""
para cada célula lógica (y,x):

    cy = y*2+1
    cx = x*2+1

    valor = 0

    se grid[cy-1][cx] == 1: valor += 1   # N
    se grid[cy][cx+1] == 1: valor += 2   # E
    se grid[cy+1][cx] == 1: valor += 4   # S
    se grid[cy][cx-1] == 1: valor += 8   # W

    converter valor para hex
    """