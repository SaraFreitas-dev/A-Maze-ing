# Themes System Documentation

This document explains the visual theme system in A-Maze-ing, including design philosophy, implementation details, and asset management.

## Overview

The theme system provides multiple visual styles for the maze experience, allowing users to switch between different aesthetic presentations while maintaining the same core functionality.

## Theme Philosophy

### Visual Consistency

Each theme maintains:
- **Coherent color palette**: All elements work together harmoniously
- **Consistent style**: Similar artistic approach across all assets
- **Clear readability**: Distinct visual separation between maze elements
- **Atmospheric mood**: Each theme evokes a specific feeling or environment

### Functional Clarity

Regardless of theme:
- **Walls vs. Paths**: Always clearly distinguishable
- **Entry/Exit points**: Prominently visible
- **Solution path**: Highlighted distinctly from exploration
- **Interactive elements**: Consistent visual feedback

## Available Themes

### Light Theme (Normal)

**Aesthetic**: Bright, clean, welcoming
**Mood**: Friendly exploration, casual gaming
**Color Palette**: 
- Bright backgrounds
- Warm floor tones
- Light wall colors
- Vibrant accents

**Visual Elements**:
- `normal_wall`: Light-colored brick or stone textures
- `normal_floor`: Warm, inviting path surfaces
- `normal_trail`: Bright breadcrumb trail
- `normal_duck`: Cheerful, colorful character
- `normal_exit`: Welcoming portal or doorway

### Dark Theme (Gothic)

**Aesthetic**: Mysterious, atmospheric, dramatic
**Mood**: Adventurous exploration, fantasy setting
**Color Palette**:
- Dark backgrounds
- Cool floor tones
- Deep wall colors
- Atmospheric accents

**Visual Elements**:
- `gothic_wall`: Dark stone, ancient textures
- `gothic_floor`: Shadowy path surfaces
- `gothic_trail`: Mystical glowing trail
- `gothic_duck`: Adventurous, fantasy-styled character
- `gothic_exit`: Magical portal or ancient doorway

## Asset Management System

### Asset Organization

```
assets/
├── imgs/                    # Source images (PNG)
│   ├── menu_background.png
│   ├── banner.jpeg
│   ├── light_wall.png
│   ├── normal_floor.png
│   ├── normal_duck.jpeg
│   ├── normal_exit.png
│   ├── normal_trail.png
│   ├── dark_wall.png
│   ├── gothic_floor.png
│   ├── gothic_duck.png
│   ├── gothic_exit.png
│   └── gothic_trail.png
└── generated/               # Processed assets (XPM)
    ├── normal_wall_55.xpm
    ├── normal_floor_55.xmp
    └── ...
```

### Dynamic Asset Generation

Assets are automatically processed at runtime:

1. **Source Processing**: PNG assets are resized to match current tile size
2. **Format Conversion**: Resized PNGs are converted to XPM for MLX
3. **Theme Loading**: Appropriate asset set loaded based on current theme
4. **Memory Management**: Assets cached for performance, cleaned up when switching

### Asset Scaling System

```python
def generate_scaled_asset(input_path, output_path, tile_size):
    """
    Resize image to match maze cell dimensions while preserving style
    """
    # Open source image
    image = Image.open(input_path)
    
    # Resize using NEAREST neighbor to maintain pixel-art aesthetic
    resized_image = image.resize((tile_size, tile_size), 
                                Image.Resampling.NEAREST)
    
    # Save resized version
    resized_image.save(output_path)
```

## Theme Implementation

### Theme Switching Logic

```python
def switch_theme(current_theme):
    """
    Switch between available themes
    """
    if current_theme == "normal":
        new_theme = "gothic"
    else:
        new_theme = "normal"
    
    # Load new theme assets
    load_theme_assets(new_theme)
    
    # Update display
    render_with_new_theme()
    
    return new_theme
```

### Asset Loading Pipeline

```python
def load_theme_assets(theme_name, tile_size):
    """
    Load complete asset set for specified theme
    """
    theme_assets = {}
    
    # Define asset types
    asset_types = ['wall', 'floor', 'trail', 'duck', 'exit', 'exit2']
    
    for asset_type in asset_types:
        # Generate scaled asset if needed
        source_path = f"assets/imgs/{theme_name}_{asset_type}.png"
        scaled_path = f"assets/generated/{theme_name}_{asset_type}_{tile_size}.png"
        xmp_path = f"assets/generated/{theme_name}_{asset_type}_{tile_size}.xpm"
        
        # Create scaled version
        if not os.path.exists(scaled_path):
            generate_scaled_asset(source_path, scaled_path, tile_size)
        
        # Convert to XPM
        if not os.path.exists(xmp_path):
            convert_to_xpm(scaled_path, xmp_path)
        
        # Load into MLX
        theme_assets[asset_type] = mlx.mlx_xpm_file_to_image(mlx_ptr, xmp_path)
    
    return theme_assets
```

## Visual Design Principles

### Color Theory Application

**Light Theme**:
- **Base**: Warm neutrals (beiges, light browns)
- **Accent**: Bright primaries (blues, greens)
- **Contrast**: High contrast for readability
- **Saturation**: Medium to high for energy

**Dark Theme**:
- **Base**: Cool darks (grays, deep blues, purples)
- **Accent**: Muted mysticals (purples, teals)
- **Contrast**: Sufficient for visibility without harshness
- **Saturation**: Lower saturation for atmospheric mood

### Pixel Art Principles

**Style Consistency**:
- Consistent pixel density across all assets
- Similar line weights and edge treatment
- Harmonious color reduction (limited palettes)
- Coherent shading and highlighting techniques

**Scaling Considerations**:
- NEAREST neighbor scaling to maintain crisp edges
- Tile sizes divisible by original pixel dimensions
- Consistent proportions across different sizes
- Clear readability at all supported scales

## Theme-Specific Features

### Background Systems

**Menu Backgrounds**:
- Each theme has custom menu background
- Automatically scaled to window dimensions
- Maintains aspect ratio and quality
- Consistent branding and mood

**Maze Backgrounds**:
- Contextual floor textures for each theme
- Seamless tiling at any scale
- Appropriate contrast with walls and characters
- Performance-optimized for real-time rendering

### Character Design

**Duck Character Evolution**:

**Normal Duck**:
- Bright, friendly colors
- Rounded, approachable features
- Clear, high-contrast details
- Cheerful expression and posture

**Gothic Duck**:
- Deeper, more mysterious colors
- Slightly more angular features
- Atmospheric shading and details
- Adventurous, determined expression

### Trail and Path Systems

**Visual Breadcrumbs**:

**Normal Trail**:
- Bright, visible markings
- Warm, inviting colors
- Clear contrast with floor
- Optimistic, progress-indicating style

**Gothic Trail**:
- Mystical, glowing effects
- Cool, atmospheric colors
- Subtle but visible against dark floors
- Magical, discovery-suggesting style

## Implementation Details

### Performance Optimization

**Asset Caching**:
- Pre-load commonly used assets
- Keep current theme assets in memory
- Lazy-load theme switch assets
- Efficient memory cleanup on theme change

**Rendering Efficiency**:
- Batch similar asset rendering
- Minimize texture switching
- Use tile-based rendering for consistent performance
- Optimize for frequent redraw scenarios

### Memory Management

```python
def cleanup_theme_assets(theme_assets):
    """
    Clean up MLX image resources for theme switch
    """
    for asset_name, img_ptr in theme_assets.items():
        if img_ptr:
            mlx.mlx_destroy_image(mlx_ptr, img_ptr)
```

### Error Handling

**Fallback Systems**:
- Default to normal theme if assets missing
- Graceful degradation if conversion fails
- Clear error messages for asset problems
- Automatic retry for transient failures

## User Experience

### Theme Switching

**Immediate Feedback**:
- Instant visual change when theme switched
- No loading delays or interruptions
- Preserved game state across theme changes
- Clear indication of active theme

**Visual Continuity**:
- Same maze layout with new appearance
- Consistent UI element positions
- Preserved solution and exploration state
- Smooth transition between themes

### Accessibility Considerations

**Contrast Requirements**:
- Both themes meet readability standards
- High contrast between functional elements
- Clear distinction between different maze components
- Visible in various lighting conditions

**Color-Blind Considerations**:
- Shape and pattern differences supplement color
- High luminance contrast for critical elements
- Multiple visual cues for important information
- Tested with color-blindness simulators

## Future Theme Possibilities

### Potential New Themes

**Retro/8-bit Theme**:
- Limited color palettes
- Chunky pixel aesthetics
- Classic gaming references
- Nostalgic chip-tune atmosphere

**Nature Theme**:
- Organic textures and colors
- Forest/garden maze aesthetics
- Natural pathway materials
- Wildlife-inspired character designs

**Sci-fi Theme**:
- Futuristic corridor designs
- Neon accent colors
- High-tech maze environments
- Robot or space-suit characters

### Extensibility Features

**Theme Definition System**:
- JSON-based theme configuration
- Easy addition of new themes
- User-customizable color schemes
- Community-shareable theme packs

**Dynamic Theme Elements**:
- Time-based theme changes
- Adaptive themes based on maze properties
- Animated theme transitions
- Seasonal or event-specific themes

## Technical Benefits

The theme system provides:

1. **Visual Variety**: Multiple aesthetic experiences
2. **User Preference**: Accommodation of different tastes
3. **Reusability**: Same rendering code for all themes
4. **Extensibility**: Easy addition of new visual styles
5. **Performance**: Efficient asset management and rendering