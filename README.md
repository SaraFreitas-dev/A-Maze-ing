
```bash

a-maze-ing # main folder
|-a_maze_ing.py # main, entrypoint
|-Makefile
|-README.md
|-maze.txt  # W E S N path
|-requirements.txt # libs for venv
|-pyproject.toml # project configuration (Python version, flake8 rules, authors, etc.)
|
|__config # folder
|  |__config.txt # KEY=VALUE (WIDTH, HEIGHT, ENTRY, etc.) values
|
|__render # folder
|  |__ __init__.py
|  |__ascii_renderer.py # visual design ascii
|  |__mlx_renderer.py # visual design mlx
|  |__ menu_design.py # visual design of the main menu
|  |__player_commands.py # make the maze playable
|
|__assets # folder - mlx
|   |__textures
|   |__fonts
|   |__42_pattern.txt # 42 in ascii design
|__utils # folder
|
|  |__ __init__.py
|  |__ directions.py # N E S W (helpers)
|  |__ errors.py # for error handling
|
|__tests # folder
|  |__ __init__.py
|  |__test_maze.py  # scripts for tests only
|  |__test_solver.py # scripts for tests only
|
|__core # folder
|  |__maze.py # maze structure (grid + cells)
|  |__generator.py # algorithm to generate maze - Class MazeGenerator
|  |__solver.py # BFS algorithm - shortest path to solve the maze
|  |__bonus_solver.py # another algorithm to solve the maze
|  |__exporter.py # convert to hex
|
|__ parsing # folder
|  |__ __init__.py
|  |__ config_parser.py # parse KEY=VALUE config file (WIDTH, HEIGHT, etc.)

```


# 🐍 Virtual Environment: Instructions

Short guide to create an isolated Python environment, install project dependencies, and manage activation/deactivation both on windows and linux.

### Create
```bash
python3 -m venv venv
```

### Activate

## Linux / macOS
```bash
source venv/bin/activate
```

## Windows (CMD)
```bash
venv\Scripts\activate
```

## Install requirements (on venv)
```bash
pip install -r requirements.txt
```

## Deactivate
```bash
deactivate
```

## Run main - Example
```bash
 python3 -m render.ascii_renderer
```

## 📦 Config Parser (parsing/config_parser.py)

#### Features:

- Reads the configuration file  
- Ignores empty lines and comments  
- Validates line format (`KEY=VALUE`)  
- Detects duplicate keys  
- Ensures all mandatory required keys are present  
- Displays clear error messages when needed  
- Converts configuration values into appropriate types (int, tuple, bool)  
- Validates values to ensure the maze can be generated correctly  

---

## 🧱 Maze (core/maze.py)

#### Features:

- Stores the maze structure and core data  
- Initializes a fully walled grid (default state)  
- Expands logical maze into a grid with walls (`2 * size + 1`)  
- Stores entry and exit coordinates  
- Provides a base structure for generation algorithms  

---

## 🌱 Maze Generator (core/generator.py)

#### Features:

- Generates a maze using the Depth-First Search (DFS) algorithm  
- Ensures all cells are reachable (full connectivity)  
- Randomizes directions to produce different maze layouts  
- Breaks walls between cells to create valid paths  
- Applies entry and exit openings on maze borders  
- Validates entry and exit positions before opening them  

---

## 🖨️ ASCII Renderer (render/ascii_renderer.py)

#### Features:

- Displays the maze in the terminal  
- Converts internal grid values into visual symbols  
- Distinguishes walls and paths (`■` / `□`)  
- Provides a simple visual representation for debugging and testing  

---

## 🚀 Main (a_maze_ing.py)

#### Features:

- Entry point of the application  
- Loads and validates configuration  
- Initializes the maze structure  
- Runs the maze generation process  
- Applies entry and exit openings  
- Renders the maze in the terminal  
- Handles errors gracefully without crashing  


## 📦 Next steps

- def solve_maze(maze: Maze) -> list[tuple[int, int]]
    Algorithm to solve the path
- def path_to_directions(path: list[tuple[int, int]]) -> str
    Converte the path into directions (W, E, S, N)
    To later add them in the maze.txt
- def maze_to_hex(maze: Maze) -> list[list[str]]
    Converte the maze to hex
- def export_maze(maze: Maze, hex_grid: list[list[str], path_str[str]]) -> None
    Export the maze (maze.txt)
...
Pos: Design / graphs, add 42 logo, unperfect_path (when perfect=false), verify maze conditions (open sizes, etc)

config
  ↓
Maze()
  ↓
dfs_generator()
  ↓
apply_entry_exit()
  ↓
check_open_areas()   !!! Maze rules complier (if needed → regenerate maze)
  ↓
if not PERFECT:
    break_walls()    ⚠️ Add extra paths
  ↓
solve_maze()         ⚠️ BFS
  ↓
path_to_directions() ⚠️ (0,1) -> (1,1) f.e. to N E W S
  ↓
maze_to_hex()        ⚠️
  ↓
export_maze()        ⚠️ Creates maze.txt
  ↓
render()             ⚠️ Add Minilibx