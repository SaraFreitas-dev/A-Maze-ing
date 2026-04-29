from core.maze import Maze
from core.generator import dfs_generator


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


if __name__ == "__main__":
    maze = Maze(5, 5, (0, 0), (5, 5))
    dfs_generator(maze)
    render(maze.grid)
