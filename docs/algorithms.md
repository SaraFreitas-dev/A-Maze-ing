# Algorithms Documentation

This document explains the algorithms used in the A-Maze-ing project for maze generation and pathfinding.

## Overview

The project uses two main algorithms:
- **DFS (Depth-First Search)** for maze generation
- **BFS (Breadth-First Search)** for maze solving and pathfinding

## DFS - Maze Generation Algorithm

### What is DFS?

Depth-First Search is a graph traversal algorithm that explores as far as possible along each branch before backtracking.

### Why DFS for Maze Generation?

DFS was chosen for maze generation because:
- **Natural maze structure**: Creates long, winding corridors
- **Perfect connectivity**: Guarantees all cells are reachable
- **Backtracking behavior**: Creates dead ends and interesting paths
- **Simplicity**: Relatively easy to implement and understand
- **Memory efficiency**: Uses stack-based recursion

### How DFS Works in Maze Generation

1. **Start**: Begin at a random cell in the maze
2. **Mark**: Mark the current cell as visited
3. **Choose**: Select a random unvisited neighbor
4. **Carve**: Remove the wall between current cell and chosen neighbor
5. **Move**: Move to the chosen neighbor
6. **Recurse**: Repeat the process from the new cell
7. **Backtrack**: When no unvisited neighbors exist, backtrack to previous cell
8. **Continue**: Repeat until all cells are visited

### DFS Implementation Details

```python
def dfs_generator(maze):
    """
    Generate maze using Depth-First Search algorithm
    """
    # Implementation creates a perfect maze with single solution path
    # Uses recursive backtracking to carve paths through walls
    # Ensures all cells are reachable from any starting point
```

### DFS Characteristics

- **Time Complexity**: O(V + E) where V = cells, E = connections
- **Space Complexity**: O(V) for the recursion stack
- **Result**: Perfect maze (exactly one path between any two points)
- **Randomness**: Uses random neighbor selection for varied results

## BFS - Pathfinding Algorithm

### What is BFS?

Breadth-First Search is a graph traversal algorithm that explores all neighbors at the current depth before moving to nodes at the next depth level.

### Why BFS for Pathfinding?

BFS was chosen for maze solving because:
- **Shortest path guarantee**: Always finds the optimal solution
- **Level-by-level exploration**: Systematic and complete
- **Animation friendly**: Can visualize exploration process
- **Deterministic**: Same maze always produces same solution

### How BFS Works in Maze Solving

1. **Initialize**: Start from entry point with empty queue
2. **Enqueue**: Add starting position to queue
3. **Explore**: For each position in queue:
   - Check all valid neighboring cells
   - Add unvisited neighbors to queue
   - Mark neighbors as visited with parent reference
4. **Track**: Keep parent references for path reconstruction
5. **Continue**: Repeat until exit is found or queue is empty
6. **Reconstruct**: Use parent references to build solution path

### BFS Implementation Details

```python
def bfs_solve_maze(maze):
    """
    Find shortest path using Breadth-First Search
    Returns both the solution path and exploration sequence
    """
    # Returns tuple: (path, explored)
    # path: shortest route from entry to exit
    # explored: all cells visited during search (for animation)
```

### BFS Characteristics

- **Time Complexity**: O(V + E) where V = cells, E = connections
- **Space Complexity**: O(V) for the queue and visited tracking
- **Optimality**: Guarantees shortest path solution
- **Completeness**: Will find solution if one exists

## Algorithm Integration

### Grid Coordinate System

The algorithms work with two coordinate systems:

**Logical Coordinates**:
- Used for maze dimensions (width × height)
- Represents actual maze cells
- Example: 10×8 maze has cells (0,0) to (9,7)

**Grid Coordinates**:
- Used for internal grid representation
- Includes walls between cells
- Size: (2×width + 1) × (2×height + 1)
- Example: 10×8 maze becomes 21×17 grid

### Perfect vs Imperfect Mazes

**Perfect Maze** (`perfect=True`):
- Generated using pure DFS
- Exactly one path between any two points
- No cycles or loops
- Guaranteed unique solution

**Imperfect Maze** (`perfect=False`):
- Starts with perfect maze from DFS
- Additional wall-breaking phase
- Creates multiple paths and cycles
- May have multiple solutions (BFS finds shortest)

## Algorithm Flow

```
1. Initialize maze grid (all walls)
2. Run DFS to generate perfect maze
3. Add entry/exit points
4. If imperfect: break additional walls
5. Validate maze structure
6. BFS to find solution path
7. Return maze + solution data
```

## Performance Characteristics

### DFS Generation
- **Speed**: Very fast, linear time
- **Memory**: Low memory usage (stack-based)
- **Quality**: Produces natural-looking mazes

### BFS Solving
- **Speed**: Fast, explores systematically  
- **Memory**: Moderate (queue and visited set)
- **Accuracy**: Always finds optimal solution

## Algorithmic Guarantees

1. **Maze Connectivity**: DFS ensures all cells reachable
2. **Solution Existence**: Every generated maze is solvable
3. **Optimal Path**: BFS guarantees shortest solution
4. **Deterministic**: Same seed produces identical results

## Visual Algorithm Behavior

- **DFS**: Creates long corridors, natural branching
- **BFS**: Explores in expanding circles from start
- **Animation**: BFS exploration can be visualized step-by-step
- **Path**: Solution highlights shortest route through maze