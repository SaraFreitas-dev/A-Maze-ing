from mazegen.MazeGenerator import MazeGenerator
from mazegen.Maze import Maze


class GameState:
    """Handles the game states / Banner and menu options"""
    def __init__(self) -> None:
        self.mode: str = "MENU"
        self.theme: str | None = None
        self.show_path: bool = False
        self.animate_bfs: bool = False
        self.playing: bool = False
        self.show_duck: bool = True
        #Bruno -> Track player is in maze grid
        self.player_x: int = 0
        self.player_y: int = 0

        self.clear_screen: bool = False
        self.reload_assets: bool = False
        self.maze: Maze | None = None
        self.path: list[tuple[int, int]] | None = None
        self.explored: list[tuple[int, int]] | None = None
        self.generator: MazeGenerator | None = None
