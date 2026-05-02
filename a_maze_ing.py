from core.maze import Maze
from core.solver import bfs_solve_maze
from core.generator import dfs_generator, apply_entry_exit, check_open_areas
from render.ascii_renderer import render
from parsing.config_parser import parse_config, get_config_path, convert_config
from utils.path_utils import path_to_directions
from utils.hex_utils import maze_to_hex
from utils.export_utils import export_maze, print_maze_file

import random
import time
import os


if __name__ == "__main__":
    try:
        config = parse_config(get_config_path())
        config = convert_config(config)

        if "SEED" in config:
            random.seed(config["SEED"])

        # Check if the maze created doesnt have more than 3x3 opened cells
        # Generate a maze following those rules
        while True:
            maze = Maze(
                config["WIDTH"],
                config["HEIGHT"],
                config["ENTRY"],
                config["EXIT"],
                config["OUTPUT_FILE"]
            )

            dfs_generator(maze)
            apply_entry_exit(maze)

            if check_open_areas(maze):
                break
        path = bfs_solve_maze(maze)
        for i in range(1, len(path) + 1):
            os.system("clear")
            render(maze.grid, maze, path[:i])
            time.sleep(0.05)
        
        export_maze(maze, path, config["OUTPUT_FILE"])
        print_maze_file(config["OUTPUT_FILE"])
    except Exception as e:
        print(f"Error: {e}")


"""
        # Print N E S W
        dir_path = path_to_directions(path)
        print("")
        print("".join(dir_path))

        # Print hex values
        hex_values = maze_to_hex(maze)
        print("")
        for line in hex_values:
            print("".join(line))
"""