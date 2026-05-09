from mazegen.MazeGenerator import MazeGenerator


class GameState:
    """Handles the game states / Banner and menu options"""
    def __init__(self) -> None:
        self.mode: str = "MENU"
        self.theme: str = None
        self.show_path: bool  = False
        self.animate_bfs: bool  = False
        self.playing: bool  = False

        self.clear_screen: bool = False
        self.reload_assets: bool = False
        self.maze: MazeGenerator = None
        self.path: MazeGenerator = None
        self.generator: MazeGenerator = None
