# MazeGen Package Documentation

This document describes the reusable `mazegen` package that can be installed via pip and used in other Python projects.

## Package Overview

The `mazegen` package provides a standalone, reusable maze generation and solving library extracted from the A-Maze-ing project. It can be installed independently and used in other projects without requiring the MLX graphics system.

## Package Requirements

Per the 42 School subject requirements:

- **Package Name**: Must be called `mazegen-*`
- **File Location**: Located at the root of the git repository  
- **File Formats**: Available as both `.tar.gz` and `.whl` formats
- **Example Filename**: `mazegen-1.0.0-py3-none-any.whl`
- **Build Requirements**: All elements needed to rebuild the package must be in the git repository

## Installation

### From Pre-built Package

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Building from Source

```bash
# In a virtual environment
pip install build wheel setuptools

# Build the package  
python -m build

# Install locally
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

## Basic Usage

### Instantiate and Use the Generator

```python
from mazegen import MazeGenerator

# Create a basic maze generator instance
generator = MazeGenerator(
    width=10,      # Maze width in cells
    height=10,     # Maze height in cells  
    entry=(0, 0),  # Entry coordinates (x, y)
    exit=(9, 9),   # Exit coordinates (x, y)
    perfect=True,  # Perfect maze (single solution)
    seed=None      # Random seed (None = random)
)

# Generate the maze
maze = generator.generate_maze()

# Solve the maze
path, explored = generator.solve("bfs")

print(f"Generated a {maze.width}x{maze.height} maze")
print(f"Solution found in {len(path)} steps")
```

## Custom Parameters

### Size Parameters

Control maze dimensions:

```python
# Small maze
small_gen = MazeGenerator(5, 5, (0, 0), (4, 4), True, None)

# Large maze  
large_gen = MazeGenerator(50, 30, (0, 0), (49, 29), False, 123)

# Custom entry/exit positions
custom_gen = MazeGenerator(15, 10, (0, 5), (14, 5), True, 42)
```

### Seed Parameter for Reproducibility

Use seeds for reproducible maze generation:

```python
# Create reproducible maze
seed = 12345
gen1 = MazeGenerator(10, 8, (0, 0), (9, 7), True, seed)
gen2 = MazeGenerator(10, 8, (0, 0), (9, 7), True, seed)

maze1 = gen1.generate_maze()
maze2 = gen2.generate_maze()

# Both mazes will be identical
assert maze1.grid == maze2.grid
print("Mazes are identical!")
```

### Perfect vs Imperfect Mazes

Control maze complexity:

```python
# Perfect maze (exactly one solution path)
perfect_maze = MazeGenerator(15, 15, (0, 0), (14, 14), perfect=True, seed=42)

# Imperfect maze (multiple solution paths possible)  
imperfect_maze = MazeGenerator(15, 15, (0, 0), (14, 14), perfect=False, seed=42)
```

## Accessing the Generated Structure

### Maze Object Properties

The `generate_maze()` method returns a `Maze` object with accessible properties:

```python
maze = generator.generate_maze()

# Maze dimensions
print(f"Logical size: {maze.width} x {maze.height}")
print(f"Grid size: {maze.grid_width} x {maze.grid_height}")

# Entry/exit points
print(f"Entry: {maze.entry}")  # (x, y) coordinates
print(f"Exit: {maze.exit}")    # (x, y) coordinates

# Grid structure access
grid = maze.grid  # 2D list representing the maze
```

### Grid Structure Format

**Important**: The maze generator module grants access to the maze structure, but it is not necessarily the same format as the output file.

```python
# Grid format details
maze = generator.generate_maze()

# Grid values
# 0 = open path/cell
# 1 = wall

# Grid dimensions  
logical_width = maze.width     # What you specified (e.g., 10)
logical_height = maze.height   # What you specified (e.g., 8)

actual_width = maze.grid_width   # Includes walls (e.g., 21 = 2*10+1)
actual_height = maze.grid_height # Includes walls (e.g., 17 = 2*8+1)

# The grid is larger than logical size to include walls
grid = maze.grid  # 2D array of size [grid_height][grid_width]
```

### Visualizing the Grid Structure

```python
def print_maze(maze):
    """Print ASCII representation of the maze"""
    for row in maze.grid:
        line = ""
        for cell in row:
            if cell == 1:
                line += "█"  # Wall
            else:
                line += " "  # Path
        print(line)

# Usage
maze = generator.generate_maze()
print_maze(maze)
```

## Accessing the Solution

### Getting Solution Path

```python
# Generate and solve maze
generator = MazeGenerator(12, 8, (0, 0), (11, 7), True, 456)
maze = generator.generate_maze()

# Solve using BFS algorithm (currently the only supported algorithm)
path, explored = generator.solve("bfs")

# Access solution data
print(f"Solution path length: {len(path)} steps")
print(f"Cells explored during search: {len(explored)}")
```

### Solution Data Structures

```python
# path: List of (x, y) coordinate tuples from entry to exit
# explored: List of (x, y) coordinate tuples of all cells explored

# Print the complete solution path
print("Solution path:")
for step, (x, y) in enumerate(path):
    print(f"  Step {step}: ({x}, {y})")

# Access specific path elements
start_pos = path[0]     # Should match maze.entry
end_pos = path[-1]      # Should match maze.exit
midpoint = path[len(path)//2]  # Middle of solution

# Check exploration
total_cells = maze.width * maze.height
exploration_percentage = len(explored) / total_cells * 100
print(f"Explored {exploration_percentage:.1f}% of maze cells")
```

### Solution Validation

```python
def validate_solution(maze, path):
    """Validate that the solution is correct"""
    if not path:
        return False, "No path found"
    
    if path[0] != maze.entry:
        return False, f"Path doesn't start at entry {maze.entry}"
    
    if path[-1] != maze.exit:
        return False, f"Path doesn't end at exit {maze.exit}"
    
    # Check path continuity
    for i in range(len(path) - 1):
        curr_x, curr_y = path[i]
        next_x, next_y = path[i + 1]
        
        # Check if adjacent (Manhattan distance = 1)
        distance = abs(next_x - curr_x) + abs(next_y - curr_y)
        if distance != 1:
            return False, f"Path not continuous at step {i}"
    
    return True, "Solution is valid"

# Usage
is_valid, message = validate_solution(maze, path)
print(message)
```

## Advanced Usage Examples

### Maze Generation Analysis

```python
def analyze_maze_generation(width, height, num_samples=10):
    """Analyze maze generation characteristics"""
    path_lengths = []
    exploration_counts = []
    
    for i in range(num_samples):
        gen = MazeGenerator(width, height, (0, 0), (width-1, height-1), 
                           perfect=True, seed=None)
        maze = gen.generate_maze()
        path, explored = gen.solve("bfs")
        
        path_lengths.append(len(path))
        exploration_counts.append(len(explored))
    
    avg_path_length = sum(path_lengths) / len(path_lengths)
    avg_exploration = sum(exploration_counts) / len(exploration_counts)
    
    print(f"Maze Analysis ({width}x{height}):")
    print(f"  Average path length: {avg_path_length:.1f}")
    print(f"  Average cells explored: {avg_exploration:.1f}")
    print(f"  Path length range: {min(path_lengths)}-{max(path_lengths)}")

# Run analysis
analyze_maze_generation(15, 15, 20)
```

### Seed-Based Maze Comparison

```python
def compare_perfect_vs_imperfect(width, height, seed):
    """Compare perfect and imperfect mazes with same seed"""
    
    # Generate perfect maze
    perfect_gen = MazeGenerator(width, height, (0, 0), (width-1, height-1),
                               perfect=True, seed=seed)
    perfect_maze = perfect_gen.generate_maze()
    perfect_path, perfect_explored = perfect_gen.solve("bfs")
    
    # Generate imperfect maze  
    imperfect_gen = MazeGenerator(width, height, (0, 0), (width-1, height-1),
                                 perfect=False, seed=seed)
    imperfect_maze = imperfect_gen.generate_maze()
    imperfect_path, imperfect_explored = imperfect_gen.solve("bfs")
    
    print(f"Maze Comparison (seed={seed}):")
    print(f"Perfect maze   - Path: {len(perfect_path)}, Explored: {len(perfect_explored)}")
    print(f"Imperfect maze - Path: {len(imperfect_path)}, Explored: {len(imperfect_explored)}")

# Run comparison
compare_perfect_vs_imperfect(20, 20, 789)
```

### Export Functionality

```python
# Export maze to file
generator = MazeGenerator(15, 10, (0, 0), (14, 9), False, 42)
maze = generator.generate_maze()
path, explored = generator.solve("bfs")

# Export to file (creates readable text format)
generator.export("my_maze.txt")
print("Maze exported to my_maze.txt")
```

## API Reference

### MazeGenerator Class

```python
class MazeGenerator:
    def __init__(self, width: int, height: int, 
                 entry: tuple[int, int], exit: tuple[int, int],
                 perfect: bool, seed: int | None)
    
    def generate_maze(self) -> Maze
    def solve(self, algorithm: str) -> tuple[list[tuple[int, int]], 
                                           list[tuple[int, int]]]
    def export(self, output_file: str) -> None
```

### Maze Class

```python
class Maze:
    width: int                    # Logical maze width
    height: int                   # Logical maze height
    grid_width: int              # Grid width including walls
    grid_height: int             # Grid height including walls
    entry: tuple[int, int]       # Entry coordinates
    exit: tuple[int, int]        # Exit coordinates
    grid: list[list[int]]        # 2D grid (0=path, 1=wall)
```

## Package Building

### Required Files

To build the package from source, the following files must be present:

```
mazegen/
├── __init__.py          # Package initialization
├── MazeGenerator.py     # Main generator class
├── Maze.py             # Maze data structure
├── solver.py           # BFS solving algorithm
├── generator.py        # DFS generation algorithm
├── setup.py            # Build configuration
└── README.md           # Package documentation
```

### Build Process

```bash
# Install build tools
pip install build wheel setuptools

# Build package (creates both .tar.gz and .whl)
python -m build

# Verify build
ls dist/
# Should show:
# mazegen-1.0.0-py3-none-any.whl
# mazegen-1.0.0.tar.gz
```

## Integration Notes

### Differences from Output File Format

The maze grid structure accessed through the API differs from the exported output file:

**API Grid Format**:
- 2D array of integers
- 0 = open path, 1 = wall
- Includes all walls in the grid
- Direct programmatic access

**Output File Format**:  
- Hexadecimal representation
- Custom encoding for maze elements
- Compact file format
- Designed for external consumption

### Dependencies

The package is designed to be self-contained with minimal dependencies:
- Python 3.10+
- No external libraries required for core functionality
- Optional: export functionality may require additional modules

### Performance Characteristics

- **Generation**: O(width × height) time complexity
- **Solving**: O(width × height) time complexity  
- **Memory Usage**: O(width × height) space complexity
- **Typical Performance**: Sub-second generation for mazes up to 100×100

This reusable package provides all the maze generation and solving capabilities of the A-Maze-ing project in a clean, pip-installable format suitable for integration into other Python projects.