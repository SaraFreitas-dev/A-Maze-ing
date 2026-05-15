# Parsing System Documentation

This document explains the configuration file parsing system used in A-Maze-ing to read and validate maze generation parameters.

## Overview

The parsing system reads configuration files in a simple key-value format and converts them into validated parameters for maze generation. It provides robust error handling, type conversion, and semantic validation.

## Configuration File Format

### Basic Structure

```ini
# Configuration file for A-Maze-ing
WIDTH=20
HEIGHT=15
ENTRY=0,5
EXIT=19,10
OUTPUT_FILE=output_maze.txt
PERFECT=True
SEED=42
```

### Format Rules

- **Line Structure**: `KEY=VALUE` format
- **Comments**: Lines starting with `#` are ignored
- **Whitespace**: Leading/trailing whitespace is ignored
- **Case Sensitivity**: Keys are case-sensitive
- **Empty Lines**: Ignored automatically

### Supported Data Types

- **Integers**: `WIDTH=20`, `SEED=42`
- **Booleans**: `PERFECT=True`, `PERFECT=False`  
- **Strings**: `OUTPUT_FILE=my_maze.txt`
- **Tuples**: `ENTRY=0,5`, `EXIT=19,14`

## Configuration Parameters

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `WIDTH` | int | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | int | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | tuple | Entry coordinates (x,y) | `ENTRY=0,5` |
| `EXIT` | tuple | Exit coordinates (x,y) | `EXIT=19,10` |
| `OUTPUT_FILE` | str | Output file path | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | bool | Perfect maze flag | `PERFECT=True` |
| `SEED` | int | Random seed | `SEED=42` |

### Parameter Validation

**WIDTH and HEIGHT**:
- Must be positive integers
- Minimum value: 1
- Maximum value: Limited by system memory
- Range validation ensures reasonable maze sizes

**ENTRY and EXIT**:
- Must be coordinate tuples (x,y)
- Must be on the border of the maze
- Cannot be the same point
- Validated against WIDTH and HEIGHT

**PERFECT**:
- Boolean value: True or False
- Case-insensitive: "true", "True", "TRUE" all accepted
- Controls maze generation algorithm behavior

**SEED**:
- Integer value for reproducible generation
- Can be any integer value
- Same seed produces identical mazes

## Implementation Details

### Parser Class Structure

```python
class ConfigParser:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = {}
        
    def parse(self) -> dict:
        """Parse configuration file and return validated config"""
        
    def _read_file(self) -> list[str]:
        """Read and preprocess configuration file"""
        
    def _parse_line(self, line: str) -> tuple[str, str] | None:
        """Parse individual configuration line"""
        
    def _validate_config(self, config: dict) -> dict:
        """Validate and convert configuration values"""
```

### File Reading Process

```python
def _read_file(self) -> list[str]:
    """Read configuration file with error handling"""
    try:
        with open(self.config_file, 'r') as file:
            lines = file.readlines()
        
        # Remove comments and empty lines
        processed_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                processed_lines.append(line)
                
        return processed_lines
        
    except FileNotFoundError:
        raise ConfigError(f"Configuration file not found: {self.config_file}")
    except PermissionError:
        raise ConfigError(f"Permission denied reading: {self.config_file}")
```

### Line Parsing Logic

```python
def _parse_line(self, line: str) -> tuple[str, str] | None:
    """Parse key=value pairs with validation"""
    if '=' not in line:
        raise ConfigError(f"Invalid line format: {line}")
    
    parts = line.split('=', 1)  # Split on first '=' only
    if len(parts) != 2:
        raise ConfigError(f"Invalid key=value format: {line}")
    
    key = parts[0].strip()
    value = parts[1].strip()
    
    if not key:
        raise ConfigError(f"Empty key in line: {line}")
    
    return key, value
```

## Type Conversion System

### Integer Conversion

```python
def _convert_int(self, value: str, key: str) -> int:
    """Convert string to integer with validation"""
    try:
        result = int(value)
        if key in ['WIDTH', 'HEIGHT'] and result <= 0:
            raise ConfigError(f"{key} must be positive, got: {result}")
        return result
    except ValueError:
        raise ConfigError(f"Invalid integer for {key}: {value}")
```

### Boolean Conversion

```python
def _convert_bool(self, value: str, key: str) -> bool:
    """Convert string to boolean (case-insensitive)"""
    value_lower = value.lower()
    if value_lower in ['true', '1', 'yes', 'on']:
        return True
    elif value_lower in ['false', '0', 'no', 'off']:
        return False
    else:
        raise ConfigError(f"Invalid boolean for {key}: {value}")
```

### Tuple Conversion

```python
def _convert_tuple(self, value: str, key: str) -> tuple[int, int]:
    """Convert string to coordinate tuple"""
    try:
        parts = value.split(',')
        if len(parts) != 2:
            raise ConfigError(f"{key} must be x,y format, got: {value}")
        
        x = int(parts[0].strip())
        y = int(parts[1].strip())
        
        return (x, y)
    except ValueError:
        raise ConfigError(f"Invalid coordinates for {key}: {value}")
```

## Validation System

### Semantic Validation

Beyond type checking, the parser performs semantic validation:

```python
def _validate_semantics(self, config: dict) -> None:
    """Validate relationships between configuration values"""
    width = config['WIDTH']
    height = config['HEIGHT']
    entry = config['ENTRY']
    exit = config['EXIT']
    
    # Validate entry point is on border
    if not self._is_on_border(entry, width, height):
        raise ConfigError(f"ENTRY {entry} must be on maze border")
    
    # Validate exit point is on border
    if not self._is_on_border(exit, width, height):
        raise ConfigError(f"EXIT {exit} must be on maze border")
    
    # Validate entry and exit are different
    if entry == exit:
        raise ConfigError("ENTRY and EXIT cannot be the same point")

def _is_on_border(self, point: tuple[int, int], width: int, height: int) -> bool:
    """Check if point is on the maze border"""
    x, y = point
    
    # Check bounds
    if x < 0 or x >= width or y < 0 or y >= height:
        return False
    
    # Check if on border
    return x == 0 or x == width-1 or y == 0 or y == height-1
```

### Duplicate Key Detection

```python
def _check_duplicates(self, lines: list[str]) -> None:
    """Detect and report duplicate configuration keys"""
    seen_keys = set()
    
    for line_num, line in enumerate(lines, 1):
        key, _ = self._parse_line(line)
        
        if key in seen_keys:
            raise ConfigError(f"Duplicate key '{key}' found at line {line_num}")
        
        seen_keys.add(key)
```

## Error Handling

### Custom Exception Class

```python
class ConfigError(Exception):
    """Custom exception for configuration parsing errors"""
    def __init__(self, message: str, line_number: int = None):
        self.message = message
        self.line_number = line_number
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.line_number:
            return f"Config error at line {self.line_number}: {self.message}"
        return f"Config error: {self.message}"
```

### Error Categories

**File Errors**:
- File not found
- Permission denied
- I/O errors

**Format Errors**:
- Invalid line format
- Missing equals sign
- Empty keys

**Type Errors**:
- Invalid integer values
- Invalid boolean values  
- Invalid coordinate format

**Semantic Errors**:
- Entry/exit not on border
- Entry and exit same point
- Invalid coordinate ranges
- Duplicate keys

### Error Recovery

The parser fails fast on errors but provides detailed error messages:

```python
try:
    config = parser.parse()
except ConfigError as e:
    print(f"Configuration error: {e}")
    print("Please check your config file and try again.")
    sys.exit(1)
```

## Usage Examples

### Basic Usage

```python
from parsing.config_parser import ConfigParser

# Parse configuration file
parser = ConfigParser("config.txt")
try:
    config = parser.parse()
    
    # Access parsed values
    width = config['WIDTH']
    height = config['HEIGHT']
    entry = config['ENTRY']
    exit = config['EXIT']
    perfect = config['PERFECT']
    seed = config['SEED']
    output_file = config['OUTPUT_FILE']
    
except ConfigError as e:
    print(f"Error parsing config: {e}")
```

### Validation Example

```python
# Example config file content
config_content = """
# Maze configuration
WIDTH=25
HEIGHT=15
ENTRY=0,7
EXIT=24,7
OUTPUT_FILE=large_maze.txt
PERFECT=False
SEED=12345
"""

# This would pass all validation checks
```

### Error Example

```python
# Example with errors
invalid_config = """
WIDTH=-5        # Error: negative width
HEIGHT=abc      # Error: invalid integer
ENTRY=50,10     # Error: outside maze bounds  
EXIT=50,10      # Error: same as entry, outside bounds
PERFECT=maybe   # Error: invalid boolean
SEED=           # Error: empty value
WIDTH=10        # Error: duplicate key
"""

# Would generate multiple validation errors
```

## Integration with Maze Generation

### Configuration to Generator

```python
def create_maze_from_config(config_file: str) -> MazeGenerator:
    """Create maze generator from configuration file"""
    parser = ConfigParser(config_file)
    config = parser.parse()
    
    generator = MazeGenerator(
        width=config['WIDTH'],
        height=config['HEIGHT'],
        entry=config['ENTRY'],
        exit=config['EXIT'],
        perfect=config['PERFECT'],
        seed=config['SEED']
    )
    
    return generator, config['OUTPUT_FILE']
```

### Default Configuration

```python
DEFAULT_CONFIG = {
    'WIDTH': 20,
    'HEIGHT': 20,
    'ENTRY': (0, 0),
    'EXIT': (19, 19),
    'OUTPUT_FILE': 'maze.txt',
    'PERFECT': True,
    'SEED': None
}

def get_config_with_defaults(config_file: str) -> dict:
    """Get configuration with fallback to defaults"""
    if not os.path.exists(config_file):
        print("Config file not found, using defaults")
        return DEFAULT_CONFIG.copy()
    
    try:
        parser = ConfigParser(config_file)
        return parser.parse()
    except ConfigError as e:
        print(f"Config error: {e}")
        print("Using default configuration")
        return DEFAULT_CONFIG.copy()
```

## Benefits

The parsing system provides:

1. **Robustness**: Comprehensive error handling and validation
2. **Flexibility**: Easy configuration file modification
3. **Type Safety**: Automatic type conversion and validation
4. **User-Friendly**: Clear error messages and documentation
5. **Extensibility**: Easy to add new configuration parameters

## Future Enhancements

Potential improvements:

- **Configuration schema validation**: JSON Schema for config structure
- **Environment variable support**: Override config with env vars
- **Configuration inheritance**: Include/extend other config files  
- **Live configuration reload**: Hot-reload config changes
- **GUI configuration editor**: Visual config file editing