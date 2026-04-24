class Maze:
    """
    Stores the maze data
    This is TEMPORARY with 0 int values - for tests
    """
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: list[list[int]] = []

        for _ in range(0, self.height):
            row: list[int] = []
            for _ in range(0, self.width):
                row.append(0)
            self.grid.append(row)
