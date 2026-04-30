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
        for dx, dy in random.sample(directions, len(directions)):
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


def apply_entry_exit(maze: Maze) -> None:
    """
    Calculate the position of the entry and exit on the expanded grid
    And open those locations
    """
    grid = maze.grid
    height = maze.height
    width = maze.width
    x1, y1 = maze.entry
    x2, y2 = maze.exit

    # Open the path / Internal cell of the maze
    (entry_x, entry_y) = (x1 * 2 + 1), (y1 * 2 + 1)
    (exit_x, exit_y) = (x2 * 2 + 1), (y2 * 2 + 1)

    grid[entry_y][entry_x] = 0
    grid[exit_y][exit_x] = 0

    # Before opening entry and exit, validate their coordinates
    if not (x1 == 0 or x1 == width - 1 or
         y1 == 0 or y1 == height - 1
    ):
        raise ValueError("Invalid entry point. Maze can't be generated.")
    if not (x2 == 0 or x2 == width - 1 or
         y2 == 0 or y2 == height - 1
    ):
        raise ValueError("Invalid exit point. Maze can't be generated.")
    
    # Open the actual entry "door"
    if x1 == 0:
        grid[entry_y][entry_x - 1] = 0
    elif x1 == maze.width - 1:
        grid[entry_y][entry_x + 1] = 0
    elif y1 == 0:
        grid[entry_y - 1][entry_x] = 0
    elif y1 == maze.height - 1:
        grid[entry_y + 1][entry_x] = 0

    # Open the actual exit "door"
    if x2 == 0:
        grid[exit_y][exit_x - 1] = 0
    elif x2 == maze.width - 1:
        grid[exit_y][exit_x + 1] = 0
    elif y2 == 0:
        grid[exit_y - 1][exit_x] = 0
    elif y2 == maze.height - 1:
        grid[exit_y + 1][exit_x] = 0


def check_open_areas(maze: Maze) -> bool:
    """
    Check if the previous generated maze complies with the 42 rules
    (No more than 2x2 or 3x3 open spaces)
    """
    grid = maze.grid
    height = maze.grid_height
    width = maze.grid_width

    for y in range(0, height - 2):
        for x in range(0, width - 2):
            open_spaces = 0
            for dy in range(0, 3):
                for dx in range(0, 3):
                    if grid[y + dy][x + dx] == 0:
                        open_spaces += 1
            if open_spaces == 9:  # found  3x3 opened cells
               return False
    return True 
