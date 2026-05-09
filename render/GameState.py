class GameState:
    """Handles the game states / Banner and menu options"""
    def __init__(self) -> None:
        self.mode = "MENU"
        self.theme = None
        self.show_path = False
        self.animate_bfs = False
        self.playing = False
        self.clear_screen = False