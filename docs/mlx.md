# MLX Integration Documentation

This document explains how MiniLibX (MLX) is integrated into the A-Maze-ing project for graphics rendering and user interaction.

## Overview

The project uses a Python wrapper for MiniLibX to handle:
- Window creation and management
- Image rendering and display
- Event handling (keyboard input)
- Real-time animation and updates
- Asset management and scaling

## MLX Architecture

### Core Components

The MLX integration is organized into several modules:

- **`render/mlx_renderer.py`**: Main MLX interface and window management
- **`render/draw_maze.py`**: Maze rendering and visualization
- **`render/menu.py`**: Menu system and banner display
- **`render/converter.py`**: Asset processing and XPM conversion
- **`render/GameState.py`**: Game state and interaction management

## MLX Setup and Initialization

### Window Creation

```python
# Initialize MLX instance
mlx = Mlx()
mlx_ptr = mlx.init()

# Create game window
win_ptr = mlx.new_window(mlx_ptr, WINDOW_WIDTH, WINDOW_HEIGHT, "A-Maze-ing")
```

### Window Properties

- **Resolution**: 1600×900 pixels (configurable)
- **Title**: "A-Maze-ing"
- **Color Depth**: 32-bit RGBA
- **Refresh Rate**: Event-driven updates

## Image System

### XPM Format

MLX requires images in XPM format. The project converts PNG assets to XPM:

```python
# Convert PNG to XPM using ImageMagick
os.system(f"magick {png_path} {xmp_path}")

# Load XPM into MLX
img_ptr, width, height = mlx.mlx_xpm_file_to_image(mlx_ptr, xmp_path)
```

### Asset Pipeline

1. **Source Images**: PNG files in `assets/imgs/`
2. **Processing**: Resize and convert to XPM in `assets/generated/`
3. **Loading**: Load XPM files into MLX image pointers
4. **Rendering**: Display images using `mlx_put_image_to_window`

### Dynamic Scaling

Assets are automatically scaled based on maze tile size:

```python
def generate_scaled_asset(input_path, output_path, tile_size):
    """Resize image to match maze cell dimensions"""
    image = Image.open(input_path)
    resized_image = image.resize((tile_size, tile_size), Image.Resampling.NEAREST)
    resized_image.save(output_path)
```

## Rendering System

### Coordinate System

MLX uses screen coordinates:
- **Origin**: Top-left corner (0, 0)
- **X-axis**: Left to right (positive)
- **Y-axis**: Top to bottom (positive)
- **Units**: Pixels

### Maze Rendering

The maze is rendered tile by tile:

```python
def render_maze_cell(mlx, win_ptr, img, x, y, tile_size):
    """Render single maze cell at screen coordinates"""
    screen_x = x * tile_size + offset_x
    screen_y = y * tile_size + offset_y
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img, screen_x, screen_y)
```

### Centering System

Mazes are automatically centered on screen:

```python
def calculate_centering_offset(maze_width, maze_height, tile_size):
    """Calculate offset to center maze in window"""
    maze_pixel_width = maze_width * tile_size
    maze_pixel_height = maze_height * tile_size
    
    offset_x = (WINDOW_WIDTH - maze_pixel_width) // 2
    offset_y = (WINDOW_HEIGHT - maze_pixel_height) // 2
    
    return offset_x, offset_y
```

## Event Handling

### Keyboard Events

MLX handles keyboard input through event hooks:

```python
def key_hook(keycode, param):
    """Handle keyboard input"""
    if keycode == KEY_ESC or keycode == ord('6'):
        # Quit application
        mlx.destroy_window(mlx_ptr, win_ptr)
        exit(0)
    elif keycode == ord('1'):
        # Regenerate maze
        regenerate_maze()
    elif keycode == ord('2'):
        # Show solution path
        show_solution()
    # ... more key handlers

# Register event hook
mlx.on_key_down(mlx_ptr, key_hook, param)
```

### Key Mappings

| Key | Action | Description |
|-----|--------|-------------|
| `1` | Regenerate | Generate new random maze |
| `2` | Show Path | Display BFS solution path |
| `3` | Show Animation | Animate BFS exploration |
| `4` | Play Mode | Manual player movement |
| `5` | Change Theme | Switch between light/dark themes |
| `6`/`ESC` | Quit | Exit application |

## Animation System

### Frame-Based Animation

The project uses time-based animation for:
- BFS exploration visualization
- Solution path drawing
- Duck movement trails
- Theme transitions

### Animation Loop

```python
def animation_loop():
    """Main animation and rendering loop"""
    while running:
        # Clear previous frame
        mlx.clear_window(mlx_ptr, win_ptr)
        
        # Update animation state
        update_animation_state()
        
        # Render current frame
        render_maze()
        render_animations()
        render_ui()
        
        # Present frame
        mlx.do_sync(mlx_ptr)
```

### BFS Animation

The BFS exploration is animated by showing cells as they're explored:

```python
def animate_bfs_exploration(explored_cells):
    """Animate BFS exploration step by step"""
    for step, cell in enumerate(explored_cells):
        # Render exploration up to current step
        render_explored_cells(explored_cells[:step+1])
        
        # Small delay for visibility
        time.sleep(ANIMATION_DELAY)
        
        # Update display
        mlx.do_sync(mlx_ptr)
```

## Memory Management

### Image Memory

MLX requires careful memory management for images:

```python
# Load image
img_ptr, w, h = mlx.mlx_xpm_file_to_image(mlx_ptr, path)

# Use image for rendering
mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, x, y)

# Clean up when done
mlx.mlx_destroy_image(mlx_ptr, img_ptr)
```

### Window Cleanup

```python
def cleanup_mlx():
    """Clean up MLX resources"""
    # Destroy images
    for img_ptr in loaded_images:
        if img_ptr:
            mlx.mlx_destroy_image(mlx_ptr, img_ptr)
    
    # Destroy window
    mlx.mlx_destroy_window(mlx_ptr, win_ptr)
    
    # Clean up MLX instance
    mlx.mlx_destroy_display(mlx_ptr)
```

## Theme System Integration

### Dynamic Asset Loading

The theme system loads different asset sets:

```python
def load_theme_assets(theme_name):
    """Load assets for specified theme"""
    theme_assets = {}
    
    asset_files = [
        f"{theme_name}_wall",
        f"{theme_name}_floor", 
        f"{theme_name}_trail",
        f"{theme_name}_duck",
        f"{theme_name}_exit"
    ]
    
    for asset in asset_files:
        path = f"assets/generated/{asset}_{tile_size}.xpm"
        theme_assets[asset] = mlx.mlx_xpm_file_to_image(mlx_ptr, path)
    
    return theme_assets
```

## Performance Considerations

### Rendering Optimization

- **Dirty Rectangle**: Only redraw changed areas
- **Asset Caching**: Keep frequently used images in memory
- **Tile-based Rendering**: Efficient for grid-based mazes
- **Batch Operations**: Group similar rendering calls

### Frame Rate

- **Target FPS**: 30-60 FPS for smooth animation
- **VSync**: Synchronize with display refresh rate
- **Efficient Updates**: Minimize unnecessary redraws

## MLX Limitations and Workarounds

### Image Format Restrictions

- **XPM Only**: MLX only supports XPM image format
- **Solution**: Convert PNG/JPEG assets to XPM using ImageMagick
- **Automation**: Automatic conversion in asset pipeline

### Color Handling

- **RGB Format**: MLX uses RGB color values
- **Alpha Channel**: Limited transparency support
- **Workaround**: Pre-composite images with backgrounds

### Platform Dependencies

- **Linux/WSL**: Primary development platform
- **Dependencies**: Requires X11 display system
- **Installation**: May need MLX library compilation

## Integration Benefits

The MLX integration provides:

1. **Real-time Rendering**: Immediate visual feedback
2. **Interactive Controls**: Responsive keyboard input
3. **Animation Support**: Smooth visual effects
4. **Asset Management**: Flexible image handling
5. **Cross-platform**: Works on Linux/WSL systems

## Troubleshooting

### Common Issues

**MLX Not Found**:
```bash
# Install MLX library
make install  # Installs MLX .whl file
```

**Image Loading Errors**:
- Verify XPM files exist in `assets/generated/`
- Check ImageMagick installation
- Run `make install` to generate assets

**Display Issues**:
- Ensure X11 forwarding enabled (WSL)
- Check display environment variables
- Verify graphics drivers