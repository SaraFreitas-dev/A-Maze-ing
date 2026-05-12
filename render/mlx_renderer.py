from mlx import Mlx
from typing import Any
from render.Assets import Assets
from render.converter import generate_all_assets
from render.draw_maze import draw_maze
from render.menu import (_prepare_menu_images, _draw_menu)
from render.GameState import GameState
from mazegen.Maze import Maze #Bruno -> Added so is_valid_move works
import os
import time


# ---------------------------------
# WINDOW
# ---------------------------------

WINDOW_WIDTH: int = 1600
WINDOW_HEIGHT: int = 900

# ---------------------------------
# GAME EVENTS
# ---------------------------------

KEY_ESC: int = 65307
KEY_1: int = 49
KEY_2: int = 50
KEY_3: int = 51
KEY_4: int = 52
KEY_5: int = 53
KEY_6: int = 54
#Bruno -> Player Movement
KEY_UP: int = 65362
KEY_DOWN: int = 65364
KEY_LEFT: int = 65361
KEY_RIGHT: int = 65363


def close(param: Any) -> None:
    """Close the window"""
    os._exit(0)


def key_hook(key: int, game: GameState, frame: list[int], param: Any) -> None:
    """Menu and banner game options"""

    if game.mode == "MENU":
        if key == KEY_1:
            game.theme = "normal"
            game.mode = "GAME"
            game.clear_screen = True
        elif key == KEY_2:
            game.theme = "gothic"
            game.mode = "GAME"
            game.clear_screen = True

    elif game.mode == "GAME":
        # STATIC ENTRY ON THE GAME
        if key == KEY_1:
            game.mode = "GAME"
            game.clear_screen = True
            game.reload_assets = True
            game.show_path = False
            game.playing = False
            game.game_won = False
            frame[0] = 0  # Reset the animation
            if game.generator is None:
                return
            game.maze = game.generator.generate_maze()
            game.path, game.explored = game.generator.solve("bfs")

        # 2 - SHOW PATH ANIMATION
        if key == KEY_2:
            game.show_path = True
            game.animate_bfs = False
            # Restart animation
            frame[0] = 0

        # 3 - SHOW PATH FINDER
        if key == KEY_3:
            game.show_path = False
            game.animate_bfs = True
            frame[0] = 0

    #Bruno -> PLAYER GAME MODE
        # 4 - PLAYER MODE
        if key == KEY_4:
            game.playing = True
            game.game_won = False
            game.show_path = False
            game.animate_bfs = False
            game.show_duck = True
            if game.maze is not None:
                game.player_x, game.player_y = game.maze.entry
                # Initialize grid position
                game.player_grid_x = game.player_x * 2 + 1
                game.player_grid_y = game.player_y * 2 + 1
            frame[0] = 0

        # 5 - CHANGE THEME
        if key == KEY_5:
            game.clear_screen = True
            game.reload_assets = True
            game.show_path = False
            game.animate_bfs = False
            game.show_duck = True
            if game.theme == "normal":
                game.theme = "gothic"
            else:
                game.theme = "normal"
            game.show_path = False

        # Handle player movement in player mode (only for arrow keys)
        if game.playing and key in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            handle_player_movement(key, game)

    # ESC | 6 - QUIT GAME
    if key == KEY_ESC or key == KEY_6:
        os._exit(0)


def handle_player_movement(key: int, game: GameState) -> None:
    """Handle arrow key movement for player mode - smooth grid movement"""
    if not game.playing or game.maze is None or game.game_won:
        return

    # Calculate new grid position (move by 1 grid step)
    new_grid_x, new_grid_y = game.player_grid_x, game.player_grid_y

    if key == KEY_UP:
        new_grid_y -= 1
    elif key == KEY_DOWN:
        new_grid_y += 1
    elif key == KEY_LEFT:
        new_grid_x -= 1
    elif key == KEY_RIGHT:
        new_grid_x += 1

    # Check bounds
    if not (0 <= new_grid_y < game.maze.grid_height and 0 <= new_grid_x < game.maze.grid_width):
        return

    # Check if position is blocked
    if game.maze.grid[new_grid_y][new_grid_x] == 1 or game.maze.grid[new_grid_y][new_grid_x] == 2:
        return

    # Update grid position
    game.player_grid_x = new_grid_x
    game.player_grid_y = new_grid_y

    # Update logical position based on new grid position
    game.player_x = (new_grid_x - 1) // 2
    game.player_y = (new_grid_y - 1) // 2

    # Check if exit reached (logical coordinates)
    if (game.player_x, game.player_y) == game.maze.exit:
        print("🎉 Congratulations! You reached the exit!")
        print("🎉 Game Won! Press 1 to play again or ESC to quit.")
        game.game_won = True
        game.playing = False  # Stop player movement


def is_valid_grid_move(grid_x: int, grid_y: int, maze: Maze) -> bool:
    """Bruno -> This function is now unused - logic moved to handle_player_movement"""
    return True  # Placeholder
    print(f"🎮 DEBUG: Checking grid position ({grid_x}, {grid_y}) = cell value {maze.grid[grid_y][grid_x] if 0 <= grid_y < maze.grid_height and 0 <= grid_x < maze.grid_width else "OUT_OF_BOUNDS"}")
    """Bruno -> Check if move is valid in grid coordinates (not wall collision)"""
    #Bruno -> Check bounds and if position is open (0 = path, 1 = wall)
    return (0 <= grid_x < maze.grid_width and 
            0 <= grid_y < maze.grid_height and 
            maze.grid[grid_y][grid_x] == 0)
    return maze.grid[grid_y][grid_x] == 0

# ---------------------------------
# TILE SIZE
# ---------------------------------

def calculate_tile_size(game: GameState) -> int:
    """
    Dynamically calculate tile size
    so the maze fits the window
    """
    if game.maze is None:
        return 32
    maze_height = game.maze.grid_height
    maze_width = game.maze.grid_width

    tile_width = (WINDOW_WIDTH // maze_width)

    tile_height = (WINDOW_HEIGHT // maze_height)

    return min(tile_width, tile_height)


# ---------------------------------
# GAME WINDOW
# ---------------------------------

def mlx_window(game: GameState) -> None:
    """Opens the game window"""
    # TILE AND WINDOW SIZE
    tile_size = calculate_tile_size(game)

    # GENERATE ASSETS
    generate_all_assets(tile_size)

    # MLX
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    win_ptr = mlx.mlx_new_window(
        mlx_ptr,
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        "A-MAZE-ING"
    )

    # ASSETS
    assets: list[Assets | None] = [None]
    menu_imgs = _prepare_menu_images(mlx, mlx_ptr)

    # DRAW
    frame = [0]
    last_time = [time.time()]

    mlx.mlx_key_hook(
        win_ptr,
        lambda key, param: key_hook(
            key,
            game,
            frame,
            param
            ),
        None
    )

    def on_loop(param: Any) -> None:
        """Loop to handle options on window"""

        # -------------------------
        # CLEAR WINDOW
        # -------------------------

        # CLEAR OLD MENU ONLY ONCE
        if game.clear_screen:
            mlx.mlx_clear_window(mlx_ptr, win_ptr)
            game.clear_screen = False

        if game.mode == "MENU":
            mlx.mlx_clear_window(
                mlx_ptr,
                win_ptr
            )

        # -------------------------
        # MENU
        # -------------------------

        if game.mode == "MENU":

            _draw_menu(
                mlx,
                mlx_ptr,
                win_ptr,
                menu_imgs
            )

        # -------------------------
        # GAME
        # -------------------------

        elif game.mode == "GAME":

            # LOAD ASSETS OR RELOAD (change theme onption)
            if game.reload_assets:
                assets[0] = None
                game.reload_assets = False
            if game.theme is None:
                return
            if assets[0] is None:

                assets[0] = Assets(
                    mlx,
                    mlx_ptr,
                    tile_size,
                    game.theme
                )

            if game.path is None:
                return
            if game.maze is None:
                return
            if game.explored is None:
                return
            if assets[0] is None:
                return

            # SHOW PATH ANIMATION - Option 2
            if game.show_path:
                now = time.time()
                if (
                    frame[0] <= len(game.path)
                    and now - last_time[0] >= 0.05
                ):

                    draw_maze(
                        game.maze,
                        mlx,
                        mlx_ptr,
                        win_ptr,
                        tile_size,
                        assets[0],
                        game.maze.grid,
                        game.path[:frame[0]]
                        if frame[0] > 0
                        else None,
                        show_duck=True,
                        duck_position=None
                    )

                    frame[0] += 1
                    last_time[0] = now

            # SHOW PATH FINDER BFS ANIMATION - Option 3
            elif game.animate_bfs:
                now = time.time()
                if (
                    frame[0] <= len(game.explored)
                    and now - last_time[0] >= 0.05
                ):

                    draw_maze(
                        game.maze,
                        mlx,
                        mlx_ptr,
                        win_ptr,
                        tile_size,
                        assets[0],
                        game.maze.grid,
                        game.explored[:frame[0]]
                        if frame[0] > 0
                        else None,
                        show_duck=False,
                        duck_position=None
                    )

                    frame[0] += 1
                    last_time[0] = now

            # STATIC MAZE
            else:
# Bruno -> refresh duck on player movement
        # Determine duck position for player mode
                  duck_position = None
                  if game.playing:
                      duck_position = (game.player_grid_y, game.player_grid_x)

                  draw_maze(
                      game.maze,
                      mlx,
                      mlx_ptr,
                      win_ptr,
                      tile_size,
                      assets[0],
                      game.maze.grid,
                      [],
                      show_duck=True,
                      duck_position=duck_position
                  )

    # WINDOW EVENTS
    mlx.mlx_hook(
        win_ptr,
        33,
        0,
        close,
        None
    )

    mlx.mlx_loop_hook(
        mlx_ptr,
        on_loop,
        None
    )

    mlx.mlx_loop(mlx_ptr)
