from mlx import Mlx
from render.Assets import Assets
from mazegen.MazeGenerator import MazeGenerator
from mazegen.Maze import Maze
from parsing.config_parser import parse_config, get_config_path, convert_config
from render.converter import generate_all_assets
import os
import time


# ---------------------------------
# WINDOW
# ---------------------------------

MAX_WINDOW_WIDTH = 1400
MAX_WINDOW_HEIGHT = 1800

# ---------------------------------
# CLOSE WINDOW
# ---------------------------------

def close(param) -> None:
    """Close the window"""

    os._exit(0)


def key_hook(key, param) -> None:
    """Close with ESC"""

    ESC_KEY = 65307

    if key == ESC_KEY:
        os._exit(0)


# ---------------------------------
# TILE SIZE
# ---------------------------------

def calculate_tile_size(
    maze: Maze) -> int:
    """
    Dynamically calculate tile size
    so the maze fits the window
    """

    maze_height = maze.grid_height

    maze_width = maze.grid_width

    tile_width = (
        MAX_WINDOW_WIDTH // maze_width
    )

    tile_height = (
        MAX_WINDOW_HEIGHT // maze_height
    )

    return min(
        tile_width,
        tile_height
    )

# ---------------------------------
# DRAW MAZE
# ---------------------------------

def draw_maze(
    maze: Maze,
    mlx: Mlx,
    mlx_ptr,
    win_ptr,
    tile_size: int,
    assets: Assets,
    grid: list[list[int]],
    path: list[tuple[int, int]] | None = None
) -> None:
    """
    Draw only the maze
    """

    # X and Y values on the expanded grid
    entry_x = maze.entry[0] * 2 + 1
    entry_y = maze.entry[1] * 2 + 1
    exit_x = maze.exit[0] * 2 + 1
    exit_y = maze.exit[1] * 2 + 1

    solved_grid = [row[:] for row in grid]
    if path is not None:
                for (y, x) in path:
                    solved_grid[y][x] = 3

    for grid_y, row in enumerate(solved_grid):

        for grid_x, cell in enumerate(row):

            # Convert grid -> pixels
            screen_x = (
                grid_x * tile_size
            )

            screen_y = (
                grid_y * tile_size
            )

            # ---------------------
            # ENTRY
            # ---------------------

            if (
                grid_x,
                grid_y
            ) == (entry_x, entry_y):
                tile = assets.floor_normal

            # ---------------------
            # EXIT
            # ---------------------

            elif (
                grid_x,
                grid_y
            ) == (exit_x, exit_y):
                tile = assets.floor_normal

            # ---------------------
            # WALL
            # --------------------
            
            elif cell == 3:
                tile = assets.duck_normal

            elif cell == 0:
                tile = assets.floor_normal

            elif cell == 2:
                tile = assets.wall_42

            # ---------------------
            # FLOOR
            # ---------------------

            else:
                tile = assets.wall

            # Draw tile
            mlx.mlx_put_image_to_window(
                mlx_ptr,
                win_ptr,
                tile,
                screen_x,
                screen_y
            )


# ---------------------------------
# MAIN WINDOW
# ---------------------------------

def mlx_window(maze: Maze,
               path: list[tuple[int, int]],
               theme: str) -> None:

    # -------------------------
    # TILE AND WINDOW SIZE
    # -------------------------

    tile_size = calculate_tile_size(
        maze
    )

    window_width = (
        maze.grid_width * tile_size
    )

    window_height = (
        maze.grid_height * tile_size
    )

    # -------------------------
    # GENERATE ASSETS
    # -------------------------

    generate_all_assets(
        tile_size
    )

    # -------------------------
    # MLX
    # -------------------------

    mlx = Mlx()

    mlx_ptr = mlx.mlx_init()

    win_ptr = mlx.mlx_new_window(
        mlx_ptr,
        window_width,
        window_height,
        "A-MAZE-ING"
    )

    mlx.mlx_hook(win_ptr, 33, 0, close, None)
    mlx.mlx_key_hook(win_ptr, key_hook, None)

    # -------------------------
    # ASSETS
    # -------------------------

    assets = Assets(
        mlx,
        mlx_ptr,
        tile_size,
        theme
    )

    # -------------------------
    # DRAW
    # -------------------------

    for i in range(1, len(path) + 1):

        draw_maze(
            maze,
            mlx,
            mlx_ptr,
            win_ptr,
            tile_size,
            assets,
            maze.grid,
            path[:i]
        )

        time.sleep(0.1)
    mlx.mlx_loop(mlx_ptr)
