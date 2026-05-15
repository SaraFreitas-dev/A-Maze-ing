# Utils and Export System Documentation

This document explains the utility functions and export system used in A-Maze-ing for data conversion, file output, and helper operations.

## Overview

The utils system provides supporting functionality for:
- Maze data export in various formats
- Coordinate and direction conversions
- Path analysis and transformation
- File I/O operations
- Hexadecimal encoding utilities

## Module Organization

### Utils Directory Structure

```
utils/
├── export_utils.py      # Main export functionality
├── hex_utils.py         # Hexadecimal conversion utilities
├── path_utils.py        # Path analysis and direction conversion
└── __init__.py         # Package initialization
```

## Export System (`export_utils.py`)

### Main Export Function

The core export functionality creates standardized maze output files:

```python
def export_maze(maze: Maze, 
                path: list[tuple[int, int]], 
                output_file: str) -> None:
    """
    Export complete maze information to text file
    
    Format:
    - Hexadecimal representation of maze cells
    - Entry and exit coordinates  
    - Solution path in NSEW directions
    """
```

### Export File Format

The exported file contains three main sections:

**1. Hexadecimal Maze Representation**:
```
# Example maze hex output
F8F8F8F8F8
8000808008
8080000008
8000808008
F8F8F8F8F8
```

**2. Entry/Exit Coordinates**:
```
0,1
4,3
```

**3. Solution Path Directions**:
```
EESSENWWN
```

### Export Implementation

```python
def export_maze(maze: Maze,
                path: list[tuple[int, int]],
                output_file: str) -> None:
    """Complete maze export implementation"""
    
    # Generate hexadecimal representation of each logical cell
    hex_values = maze_to_hex(maze)
    
    # Extract entry/exit coordinates
    entry_y, entry_x = maze.entry
    exit_y, exit_x = maze.exit
    
    # Convert solution path to directional instructions
    dir_path = path_to_directions(path)
    
    # Write to output file
    with open(output_file, "w") as file:
        # Write hex maze representation
        for line in hex_values:
            file.write("".join(line) + "\n")
        
        # Write coordinates
        file.write(f"\n{entry_y},{entry_x}\n")
        file.write(f"{exit_y},{exit_x}\n")
        
        # Write solution directions
        file.write("".join(dir_path) + "\n")
```

### File Reading Utility

```python
def print_maze_file(output_file: str) -> None:
    """Read and display maze file contents"""
    try:
        with open(output_file, "r") as file:
            for line in file:
                print(line, end="")
    except (FileNotFoundError, PermissionError, Exception) as e:
        print(f"print_maze_file() failed -> {e}")
```

## Hexadecimal Conversion System (`hex_utils.py`)

### Maze to Hex Conversion

Converts the 2D maze grid to hexadecimal representation:

```python
def maze_to_hex(maze: Maze) -> list[list[str]]:
    """
    Convert maze logical cells to hexadecimal values
    
    Each logical cell (not grid cell) gets a hex value
    representing the walls around it
    """
    
    hex_grid = []
    
    for y in range(maze.height):
        hex_row = []
        for x in range(maze.width):
            # Calculate hex value for this logical cell
            hex_value = calculate_cell_hex(maze, x, y)
            hex_row.append(f"{hex_value:02X}")
        hex_grid.append(hex_row)
    
    return hex_grid
```

### Cell Hex Calculation

```python
def calculate_cell_hex(maze: Maze, logical_x: int, logical_y: int) -> int:
    """
    Calculate hexadecimal value for a logical maze cell
    
    Hex value represents walls around the cell:
    - Bit 0: North wall
    - Bit 1: East wall  
    - Bit 2: South wall
    - Bit 3: West wall
    """
    
    # Convert logical coordinates to grid coordinates
    grid_x = logical_x * 2 + 1
    grid_y = logical_y * 2 + 1
    
    hex_value = 0
    
    # Check each direction for walls
    # North wall
    if grid_y > 0 and maze.grid[grid_y - 1][grid_x] == 1:
        hex_value |= 0x01
    
    # East wall
    if grid_x < maze.grid_width - 1 and maze.grid[grid_y][grid_x + 1] == 1:
        hex_value |= 0x02
    
    # South wall
    if grid_y < maze.grid_height - 1 and maze.grid[grid_y + 1][grid_x] == 1:
        hex_value |= 0x04
    
    # West wall
    if grid_x > 0 and maze.grid[grid_y][grid_x - 1] == 1:
        hex_value |= 0x08
    
    # Add base value for proper hex representation
    hex_value |= 0xF0  # High nibble always set
    
    return hex_value
```

### Hex Value Meaning

The hexadecimal system encodes wall information:

| Hex | Binary  | Walls Present | Description |
|-----|---------|---------------|-------------|
| F0  | 11110000 | None | Open cell (no walls) |
| F1  | 11110001 | North | North wall only |
| F2  | 11110010 | East | East wall only |
| F3  | 11110011 | North, East | Corner walls |
| F4  | 11110100 | South | South wall only |
| F8  | 11111000 | West | West wall only |
| FF  | 11111111 | All | Completely enclosed |

## Path Conversion System (`path_utils.py`)

### Path to Directions

Converts coordinate path to directional instructions:

```python
def path_to_directions(path: list[tuple[int, int]]) -> list[str]:
    """
    Convert coordinate path to NSEW directional moves
    
    Args:
        path: List of (x, y) coordinates from entry to exit
    
    Returns:
        List of direction strings ('N', 'S', 'E', 'W')
    """
    
    if len(path) < 2:
        return []
    
    directions = []
    
    for i in range(len(path) - 1):
        curr_x, curr_y = path[i]
        next_x, next_y = path[i + 1]
        
        # Calculate movement direction
        dx = next_x - curr_x
        dy = next_y - curr_y
        
        # Convert to cardinal direction
        if dx == 1 and dy == 0:
            directions.append('E')  # East
        elif dx == -1 and dy == 0:
            directions.append('W')  # West
        elif dx == 0 and dy == 1:
            directions.append('S')  # South
        elif dx == 0 and dy == -1:
            directions.append('N')  # North
        else:
            # Invalid move (not adjacent)
            raise ValueError(f"Invalid path step from {path[i]} to {path[i+1]}")
    
    return directions
```

### Direction Validation

```python
def validate_path_continuity(path: list[tuple[int, int]]) -> bool:
    """Validate that path consists of adjacent steps only"""
    
    for i in range(len(path) - 1):
        curr_x, curr_y = path[i]
        next_x, next_y = path[i + 1]
        
        # Check Manhattan distance
        distance = abs(next_x - curr_x) + abs(next_y - curr_y)
        
        if distance != 1:
            return False
    
    return True
```

### Path Analysis Utilities

```python
def analyze_path(path: list[tuple[int, int]]) -> dict:
    """Analyze path characteristics"""
    
    if not path:
        return {'length': 0, 'directions': [], 'turns': 0}
    
    directions = path_to_directions(path)
    
    # Count direction changes (turns)
    turns = 0
    for i in range(len(directions) - 1):
        if directions[i] != directions[i + 1]:
            turns += 1
    
    # Direction frequency
    direction_count = {
        'N': directions.count('N'),
        'S': directions.count('S'), 
        'E': directions.count('E'),
        'W': directions.count('W')
    }
    
    return {
        'length': len(path),
        'steps': len(directions),
        'directions': directions,
        'turns': turns,
        'direction_frequency': direction_count,
        'dominant_direction': max(direction_count, key=direction_count.get)
    }
```

## Coordinate System Utilities

### Grid Coordinate Conversion

```python
def logical_to_grid_coords(logical_x: int, logical_y: int) -> tuple[int, int]:
    """Convert logical maze coordinates to grid coordinates"""
    grid_x = logical_x * 2 + 1
    grid_y = logical_y * 2 + 1
    return grid_x, grid_y

def grid_to_logical_coords(grid_x: int, grid_y: int) -> tuple[int, int]:
    """Convert grid coordinates to logical maze coordinates"""
    logical_x = (grid_x - 1) // 2
    logical_y = (grid_y - 1) // 2
    return logical_x, logical_y
```

### Boundary Checking

```python
def is_valid_logical_coord(x: int, y: int, maze: Maze) -> bool:
    """Check if logical coordinates are within maze bounds"""
    return 0 <= x < maze.width and 0 <= y < maze.height

def is_valid_grid_coord(x: int, y: int, maze: Maze) -> bool:
    """Check if grid coordinates are within grid bounds"""
    return 0 <= x < maze.grid_width and 0 <= y < maze.grid_height
```

## File System Utilities

### Safe File Operations

```python
def safe_write_file(content: str, filepath: str) -> bool:
    """Safely write content to file with error handling"""
    try:
        # Create directory if needed
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Write file with backup
        backup_path = filepath + ".bak"
        
        # Create backup if file exists
        if os.path.exists(filepath):
            shutil.copy2(filepath, backup_path)
        
        # Write new content
        with open(filepath, 'w') as f:
            f.write(content)
        
        # Remove backup on success
        if os.path.exists(backup_path):
            os.remove(backup_path)
        
        return True
        
    except Exception as e:
        print(f"Error writing file {filepath}: {e}")
        
        # Restore backup if available
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, filepath)
            os.remove(backup_path)
        
        return False
```

### File Validation

```python
def validate_output_file(filepath: str) -> tuple[bool, str]:
    """Validate that output file can be written"""
    
    try:
        # Check directory exists or can be created
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Check write permissions
        test_file = filepath + ".test"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        
        return True, "File path is valid"
        
    except PermissionError:
        return False, f"Permission denied: {filepath}"
    except Exception as e:
        return False, f"Invalid file path: {e}"
```

## Export Format Variations

### Alternative Export Formats

The export system can be extended to support multiple output formats:

```python
def export_maze_json(maze: Maze, path: list[tuple[int, int]], 
                    output_file: str) -> None:
    """Export maze in JSON format"""
    
    maze_data = {
        'dimensions': {'width': maze.width, 'height': maze.height},
        'entry': maze.entry,
        'exit': maze.exit,
        'grid': maze.grid,
        'solution': {
            'path': path,
            'directions': path_to_directions(path),
            'length': len(path)
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(maze_data, f, indent=2)

def export_maze_csv(maze: Maze, path: list[tuple[int, int]], 
                   output_file: str) -> None:
    """Export maze in CSV format"""
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Type', 'Data'])
        writer.writerow(['Dimensions', f"{maze.width}x{maze.height}"])
        writer.writerow(['Entry', f"{maze.entry[0]},{maze.entry[1]}"])
        writer.writerow(['Exit', f"{maze.exit[0]},{maze.exit[1]}"])
        
        # Write solution path
        for i, (x, y) in enumerate(path):
            writer.writerow(['Path', f"Step {i}: ({x},{y})"])
```

## Performance Optimization

### Batch Processing

```python
def export_multiple_mazes(maze_data_list: list, base_filename: str) -> None:
    """Export multiple mazes efficiently"""
    
    for i, (maze, path) in enumerate(maze_data_list):
        output_file = f"{base_filename}_{i:03d}.txt"
        export_maze(maze, path, output_file)
        print(f"Exported maze {i+1}/{len(maze_data_list)}")
```

### Memory Efficient Export

```python
def export_large_maze_stream(maze: Maze, path: list[tuple[int, int]], 
                            output_file: str) -> None:
    """Stream large maze export to avoid memory issues"""
    
    with open(output_file, 'w') as f:
        # Stream hex values row by row
        for y in range(maze.height):
            hex_row = []
            for x in range(maze.width):
                hex_value = calculate_cell_hex(maze, x, y)
                hex_row.append(f"{hex_value:02X}")
            f.write("".join(hex_row) + "\n")
        
        # Write coordinates and path
        f.write(f"\n{maze.entry[1]},{maze.entry[0]}\n")
        f.write(f"{maze.exit[1]},{maze.exit[0]}\n")
        f.write("".join(path_to_directions(path)) + "\n")
```

## Error Handling and Validation

### Export Validation

```python
def validate_export_data(maze: Maze, path: list[tuple[int, int]]) -> list[str]:
    """Validate data before export"""
    
    errors = []
    
    # Validate maze structure
    if not maze or not maze.grid:
        errors.append("Invalid maze structure")
    
    # Validate path
    if not path:
        errors.append("Empty solution path")
    elif path[0] != maze.entry:
        errors.append("Path doesn't start at entry")
    elif path[-1] != maze.exit:
        errors.append("Path doesn't end at exit")
    
    # Validate path continuity
    if not validate_path_continuity(path):
        errors.append("Path contains non-adjacent steps")
    
    return errors
```

### Robust Export Function

```python
def robust_export_maze(maze: Maze, path: list[tuple[int, int]], 
                      output_file: str) -> tuple[bool, str]:
    """Export maze with comprehensive error handling"""
    
    try:
        # Validate input data
        validation_errors = validate_export_data(maze, path)
        if validation_errors:
            return False, f"Validation failed: {'; '.join(validation_errors)}"
        
        # Validate output path
        path_valid, path_error = validate_output_file(output_file)
        if not path_valid:
            return False, path_error
        
        # Perform export
        export_maze(maze, path, output_file)
        
        # Verify export success
        if not os.path.exists(output_file):
            return False, "Export file was not created"
        
        return True, "Export successful"
        
    except Exception as e:
        return False, f"Export failed: {e}"
```

## Integration Benefits

The utils and export system provides:

1. **Standardized Output**: Consistent maze file format
2. **Data Validation**: Robust error checking and validation
3. **Format Flexibility**: Support for multiple export formats
4. **Performance**: Efficient processing for large mazes
5. **Integration**: Seamless connection with maze generation
6. **Debugging**: Human-readable output for analysis

The system ensures reliable data export while maintaining flexibility for different use cases and output requirements.