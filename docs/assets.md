# Asset Management Documentation

This document explains how A-Maze-ing manages visual assets, including the conversion pipeline, dynamic scaling system, and theme organization.

## Overview

The asset management system handles the conversion and processing of visual assets to support:
- Multiple themes and visual styles
- Dynamic scaling for different maze sizes
- MLX-compatible image formats (XPM)
- Efficient loading and memory management

## Asset Pipeline Architecture

### Pipeline Flow

```
Source Assets (PNG/JPEG) → Scaling → Format Conversion → MLX Loading
     ↓                       ↓            ↓              ↓
assets/imgs/          PIL resize    ImageMagick      MLX pointers
                   (Python/Pillow)   (magick cmd)   (mlx_xpm_file_to_image)
                        ↓              ↓               ↓
              assets/generated/   .xpm files    Memory-loaded images
```

### Directory Structure

```
assets/
├── imgs/                     # Source images (version controlled)
│   ├── menu_background.png   # Menu background image
│   ├── banner.jpeg          # Game banner image
│   │
│   ├── light_wall.png       # Light theme wall texture
│   ├── normal_floor.png     # Light theme floor texture  
│   ├── normal_duck.jpeg     # Light theme character
│   ├── normal_exit.png      # Light theme exit portal
│   ├── normal_exit2.png     # Light theme exit animation frame
│   ├── normal_trail.png     # Light theme breadcrumb trail
│   │
│   ├── dark_wall.png        # Dark theme wall texture
│   ├── gothic_floor.png     # Dark theme floor texture
│   ├── gothic_duck.png      # Dark theme character
│   ├── gothic_exit.png      # Dark theme exit portal
│   ├── gothic_exit2.png     # Dark theme exit animation frame
│   └── gothic_trail.png     # Dark theme breadcrumb trail
│
└── generated/               # Processed assets (created at runtime)
    ├── menu_bgnew_1600x900.png
    ├── menu_bgnew_1600x900.xpm
    ├── banner_1600x180.png
    ├── banner_1600x180.xpm
    ├── normal_wall_55.jpeg
    ├── normal_wall_55.xpm
    ├── normal_floor_55.png
    ├── normal_floor_55.xpm
    └── ... (all scaled and converted assets)
```

## Asset Types and Categories

### Menu and UI Assets

**Menu Background**:
- **Source**: `menu_background.png`
- **Purpose**: Main menu background
- **Processing**: Scaled to window dimensions (1600×900)
- **Format**: PNG → XPM conversion

**Banner Image**:
- **Source**: `banner.jpeg`
- **Purpose**: Game banner with menu options
- **Processing**: Cropped and scaled to banner dimensions
- **Special handling**: Smart cropping to remove black borders

### Maze Element Assets

**Wall Textures**:
- **Light Theme**: `light_wall.png`
- **Dark Theme**: `dark_wall.png`
- **Purpose**: Maze wall rendering
- **Scaling**: Resized to match maze tile size

**Floor Textures**:
- **Light Theme**: `normal_floor.png`
- **Dark Theme**: `gothic_floor.png`
- **Purpose**: Walkable maze path rendering
- **Scaling**: Tile-size dependent

**Character Sprites**:
- **Light Theme**: `normal_duck.jpeg`
- **Dark Theme**: `gothic_duck.png`
- **Purpose**: Player/pathfinder character
- **Animation**: Single frame, positioned dynamically

**Exit Portals**:
- **Light Theme**: `normal_exit.png`, `normal_exit2.png`
- **Dark Theme**: `gothic_exit.png`, `gothic_exit2.png`
- **Purpose**: Maze exit point visualization
- **Animation**: Two frames for portal animation

**Trail Markers**:
- **Light Theme**: `normal_trail.png`
- **Dark Theme**: `gothic_trail.png`  
- **Purpose**: Solution path visualization
- **Rendering**: Overlaid on floor tiles

## Dynamic Scaling System

### Tile Size Calculation

The system calculates appropriate tile sizes based on maze dimensions:

```python
def calculate_tile_size(maze_width: int, maze_height: int, 
                       window_width: int, window_height: int) -> int:
    """Calculate optimal tile size to fit maze in window"""
    
    # Reserve space for UI elements
    available_width = window_width - UI_PADDING
    available_height = window_height - BANNER_HEIGHT - UI_PADDING
    
    # Calculate maximum tile size that fits
    max_tile_width = available_width // maze_width
    max_tile_height = available_height // maze_height
    
    # Use the smaller dimension to ensure fit
    tile_size = min(max_tile_width, max_tile_height)
    
    # Ensure minimum readable size
    return max(tile_size, MIN_TILE_SIZE)
```

### Asset Scaling Process

```python
def generate_scaled_asset(input_path: str, output_path: str, tile_size: int) -> None:
    """Resize image to specified tile size preserving pixel art style"""
    
    # Open source image
    image = Image.open(input_path)
    
    # Resize using NEAREST neighbor for pixel-perfect scaling
    resized_image = image.resize(
        (tile_size, tile_size),
        Image.Resampling.NEAREST  # Maintains crisp pixel art
    )
    
    # Save resized image
    resized_image.save(output_path)
```

### Scaling Quality Preservation

**NEAREST Neighbor Resampling**:
- Preserves pixel art aesthetic
- Maintains sharp edges
- No blur or smoothing artifacts
- Suitable for geometric patterns

**Alternative Resampling (for photos)**:
- LANCZOS for high-quality photo scaling
- Used for menu backgrounds
- Provides smooth gradients
- Better for complex imagery

## Format Conversion Pipeline

### PNG/JPEG to XPM Conversion

MLX requires XPM format images. The conversion process:

```python
def convert_to_xpm(png_path: str, xmp_path: str) -> None:
    """Convert PNG to XPM using ImageMagick"""
    
    # Use ImageMagick 'magick' command for conversion
    result = os.system(f"magick {png_path} {xmp_path}")
    
    if result != 0:
        raise ConversionError(f"Failed to convert {png_path} to XPM")
```

### XPM Format Benefits

- **MLX Compatibility**: Native format for MiniLibX
- **Color Accuracy**: Preserves exact color values
- **Transparency**: Supports transparent pixels
- **Text-based**: Human-readable format for debugging

### Batch Processing

All assets for a given tile size are processed together:

```python
def generate_all_assets(tile_size: int) -> None:
    """Generate all scaled assets for specified tile size"""
    
    os.makedirs("assets/generated", exist_ok=True)
    
    # Define all asset types and themes
    asset_configs = [
        # Menu assets
        ("menu_background", None, (WINDOW_WIDTH, WINDOW_HEIGHT)),
        ("banner", None, (WINDOW_WIDTH, BANNER_HEIGHT)),
        
        # Maze assets - Normal theme
        ("light_wall", "normal", (tile_size, tile_size)),
        ("normal_floor", "normal", (tile_size, tile_size)),
        ("normal_duck", "normal", (tile_size, tile_size)),
        ("normal_exit", "normal", (tile_size, tile_size)),
        ("normal_exit2", "normal", (tile_size, tile_size)),
        ("normal_trail", "normal", (tile_size, tile_size)),
        
        # Maze assets - Gothic theme  
        ("dark_wall", "gothic", (tile_size, tile_size)),
        ("gothic_floor", "gothic", (tile_size, tile_size)),
        ("gothic_duck", "gothic", (tile_size, tile_size)),
        ("gothic_exit", "gothic", (tile_size, tile_size)),
        ("gothic_exit2", "gothic", (tile_size, tile_size)),
        ("gothic_trail", "gothic", (tile_size, tile_size)),
    ]
    
    for asset_name, theme, dimensions in asset_configs:
        process_asset(asset_name, theme, dimensions)
```

## Loading and Memory Management

### Asset Loading

```python
def load_theme_assets(theme_name: str, tile_size: int) -> dict:
    """Load complete asset set for theme into memory"""
    
    theme_assets = {}
    asset_types = ['wall', 'floor', 'trail', 'duck', 'exit', 'exit2']
    
    for asset_type in asset_types:
        xmp_path = f"assets/generated/{theme_name}_{asset_type}_{tile_size}.xpm"
        
        if os.path.exists(xmp_path):
            # Load into MLX memory
            img_ptr, width, height = mlx.mlx_xpm_file_to_image(mlx_ptr, xmp_path)
            theme_assets[asset_type] = img_ptr
        else:
            print(f"Warning: Asset not found: {xmp_path}")
    
    return theme_assets
```

### Memory Cleanup

```python
def cleanup_theme_assets(theme_assets: dict) -> None:
    """Free MLX image memory for asset cleanup"""
    
    for asset_name, img_ptr in theme_assets.items():
        if img_ptr:
            mlx.mlx_destroy_image(mlx_ptr, img_ptr)
            
    theme_assets.clear()
```

### Caching Strategy

**Runtime Caching**:
- Keep current theme assets in memory
- Pre-load common tile sizes
- Lazy-load alternative themes
- Clear unused assets periodically

**File System Caching**:
- Generated assets persist between runs
- Only regenerate if source changed
- Check file timestamps for freshness
- Clean up old generated assets

## Special Asset Processing

### Menu Background Processing

```python
def process_menu_background(tile_size: int) -> None:
    """Process menu background with special scaling"""
    
    source_path = "assets/imgs/menu_background.png"
    output_png = f"assets/generated/menu_bgnew_{WINDOW_WIDTH}x{WINDOW_HEIGHT}.png"
    output_xmp = output_png.replace('.png', '.xpm')
    
    if not os.path.exists(output_xmp):
        # Scale to window dimensions
        if not os.path.exists(output_png):
            src = Image.open(source_path)
            resized = src.resize(
                (WINDOW_WIDTH, WINDOW_HEIGHT),
                Image.Resampling.LANCZOS  # High quality for backgrounds
            )
            resized.save(output_png)
        
        # Convert to XPM
        convert_to_xpm(output_png, output_xmp)
```

### Banner Smart Cropping

```python
def process_banner_image() -> None:
    """Process banner with smart cropping to remove borders"""
    
    banner_height = 180
    source_path = "assets/imgs/banner.jpeg"
    output_png = f"assets/generated/banner_{WINDOW_WIDTH}x{banner_height}.png"
    output_xmp = output_png.replace('.png', '.xmp')
    
    if not os.path.exists(output_xmp):
        if not os.path.exists(output_png):
            src = Image.open(source_path)
            
            # Convert to RGB for consistency
            if src.mode != 'RGB':
                src = src.convert('RGB')
            
            # Smart crop to remove black borders
            width, height = src.size
            crop_top = int(height * 0.35)    # Remove top 35%
            crop_bottom = int(height * 0.65)  # Remove bottom 35%
            
            cropped = src.crop((0, crop_top, width, crop_bottom))
            
            # Resize to banner dimensions
            resized = cropped.resize(
                (WINDOW_WIDTH, banner_height),
                Image.Resampling.LANCZOS
            )
            resized.save(output_png)
        
        # Convert to XPM
        convert_to_xpm(output_png, output_xmp)
```

## Error Handling and Validation

### Asset Validation

```python
def validate_source_assets() -> list[str]:
    """Validate that all required source assets exist"""
    
    missing_assets = []
    required_assets = [
        "assets/imgs/menu_background.png",
        "assets/imgs/banner.jpeg",
        "assets/imgs/light_wall.png",
        "assets/imgs/normal_floor.png",
        "assets/imgs/normal_duck.jpeg",
        "assets/imgs/normal_exit.png",
        "assets/imgs/normal_exit2.png", 
        "assets/imgs/normal_trail.png",
        "assets/imgs/dark_wall.png",
        "assets/imgs/gothic_floor.png",
        "assets/imgs/gothic_duck.png",
        "assets/imgs/gothic_exit.png",
        "assets/imgs/gothic_exit2.png",
        "assets/imgs/gothic_trail.png"
    ]
    
    for asset_path in required_assets:
        if not os.path.exists(asset_path):
            missing_assets.append(asset_path)
    
    return missing_assets
```

### Conversion Error Handling

```python
def safe_convert_to_xmp(png_path: str, xmp_path: str) -> bool:
    """Safely convert PNG to XMP with error handling"""
    
    try:
        # Check source exists
        if not os.path.exists(png_path):
            print(f"Error: Source file not found: {png_path}")
            return False
        
        # Run conversion
        result = os.system(f"magick {png_path} {xmp_path}")
        
        if result != 0:
            print(f"Error: ImageMagick conversion failed for {png_path}")
            return False
        
        # Verify output created
        if not os.path.exists(xmp_path):
            print(f"Error: XMP file not created: {xmp_path}")
            return False
        
        return True
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False
```

## Performance Optimization

### Lazy Loading

Assets are loaded on-demand:
- Only load assets for current theme
- Generate scaled assets when needed
- Cache frequently used assets
- Free unused assets from memory

### Parallel Processing

For large asset sets:
- Process multiple assets concurrently
- Use thread pool for I/O operations
- Batch conversion operations
- Progress indication for long operations

### Storage Efficiency

- Compress generated PNG files
- Remove intermediate files after XMP conversion
- Periodic cleanup of old generated assets
- Size-based asset cache limits

## Integration with Rendering

### Asset Loading Pipeline

```python
def prepare_maze_rendering(maze_width: int, maze_height: int, theme: str) -> dict:
    """Prepare all assets needed for maze rendering"""
    
    # Calculate optimal tile size
    tile_size = calculate_tile_size(maze_width, maze_height, 
                                  WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # Generate assets if needed
    generate_all_assets(tile_size)
    
    # Load theme assets into memory
    theme_assets = load_theme_assets(theme, tile_size)
    
    # Load menu assets
    menu_assets = load_menu_assets()
    
    return {
        'theme_assets': theme_assets,
        'menu_assets': menu_assets,
        'tile_size': tile_size
    }
```

### Rendering Integration

The asset system integrates seamlessly with the rendering pipeline:
- Assets are pre-loaded before rendering begins
- Theme switching triggers asset reload
- Tile size changes trigger asset regeneration
- Memory management prevents resource leaks

## Future Enhancements

### Potential Improvements

**Asset Compression**:
- Lossless PNG compression for generated assets
- Asset bundling for faster loading
- Progressive loading for large asset sets

**Format Support**:
- Additional input formats (GIF, WebP)
- Vector graphics support (SVG)
- Animated asset support

**Theme Extensions**:
- User-provided theme assets
- Theme asset validation
- Hot-reloading of theme changes
- Theme asset editor/preview tools

The asset management system provides a robust foundation for visual content in A-Maze-ing, ensuring high-quality rendering across different themes and maze sizes while maintaining performance and memory efficiency.