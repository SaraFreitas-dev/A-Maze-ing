from core.maze import Maze
from core.generator import dfs_generator, apply_entry_exit, check_open_areas
from render.ascii_renderer import render
from parsing.config_parser import parse_config, get_config_path, convert_config
import random


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
                config["EXIT"]
            )

            dfs_generator(maze)
            apply_entry_exit(maze)

            if check_open_areas(maze):
                break
        render(maze.grid)

    except Exception as e:
        print(f"Error: {e}")
