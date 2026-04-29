from .maze import Maze
import random


def dfs_generator(maze: Maze) -> None:
    """
    Generates a maze with the DFS algorithm
    And visits all cells
    """
    grid = maze.grid
    height = maze.grid_height
    width = maze.grid_width
    directions = [
        (0, -1),  # UP
        (0, 1),   # DOWN
        (-1, 0),  # LEFT
        (1, 0)    # RIGHT
    ]

    x, y = 1, 1

    def dfs(x: int, y: int) -> None:
        """Makes sure every cell is visited"""
        grid[y][x] = 0
        random.shuffle(directions)

        for dx, dy in directions:
            (nx, ny) = (x + dx*2), (y + dy*2)
            if (
                (0 <= nx < width) and (0 <= ny < height)
                and grid[ny][nx] == 1
            ):  # Not visited
                wall_x = x + dx
                wall_y = y + dy
                grid[wall_y][wall_x] = 0
                dfs(nx, ny)
    dfs(x, y)
