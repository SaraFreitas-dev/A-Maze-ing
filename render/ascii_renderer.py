def render(grid: list[list[int]]) -> None:
    """
    TEMPORARY - 0 prints . / 1 prints #
    """
    for row in grid:
        line = ""
        for cell in row:
            if cell == 0:
                line += "."
            else:
                line += "#"
        print(line)
