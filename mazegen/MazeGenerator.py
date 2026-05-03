from collections import deque
import random, time, os
from mazegen.Maze import Maze
from mazegen.solver import bfs_solve_maze
from mazegen.generator import (dfs_generator, apply_entry_exit,
                               check_open_areas, break_walls)
from render.ascii_renderer import render_ascii
from utils.export_utils import export_maze


class MazeGenerator:
    """
    Calls all needed functions to generate the maze:
    dfs to create a random perfect path
    adds the entry and exit cells
    if the maze is not perfect, then it "breaks walls"
    to create extra paths
    Calls the algorithm to solve and show the solution
    exports the info to the output_maze.txt file
    """
    def __init__(self,
                 width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 perfect: bool,
                 seed: int | None) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed= seed
    
    def generate_maze(self) -> Maze:
        """
        Generate a maze with dfs
        Check if all conditions apply with check_open_areas
        If not, generate another maze
        Add the entry and exit cells
        """
        try:
            if self.seed is not None:
                random.seed(self.seed)

            while True:
                maze = Maze(
                    self.width,
                    self.height,
                    self.entry,
                    self.exit
                )
                dfs_generator(maze)
                apply_entry_exit(maze)

                if not self.perfect:
                    break_walls(maze, [])

                if check_open_areas(maze):
                    break

            self.maze = maze
        except (ValueError, Exception) as e:
            print(f"generate_maze(): {e}")
        return maze

    def solve(self, algorithm: str) -> list[tuple[int, int]]:
        """
        Checks for the algorithm to apply,
        and uses it to solve the maze
        """
        if algorithm == "bfs":
            path = bfs_solve_maze(self.maze)
        else:
            raise ValueError("solve(): No algorithm found with that name.")
        self.path = path
        return path
    
    def render(self):
        """
        Renders the maze and shows it on the terminal
        """
        try:
            for i in range(1, len(self.path) + 1):
                    os.system("clear")
                    render_ascii(self.maze.grid, self.maze, self.path[:i])
                    time.sleep(0.05)
        except Exception:
            print("render(): Failed to show the maze.")
    
    def export(self, output_file: str) -> None:
        """
        Exports the information from the maze to
        the output_maze.txt file
        """
        export_maze(self.maze, self.path, output_file)
