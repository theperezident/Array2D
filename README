# array2D Library

A simple Python library for working with 2D points and grids.

## Features
- Point class with coordinate management and data storage
- Array2D class for grid-based data storage
- Optional boundary wrapping (torus topology)
- Fast dictionary-based lookups
- Cardinal direction-based movement system

## Usage
```python
from point2d import Point, Array2D, Direction

# Create a grid
grid = Array2D(rows=10, cols=10, defaultValue="Maverick")

# Set some data
grid.setData((5, 5), "Goose")

# Create a point and move it
point = Point((0, 0), data="Rooster")
point.setMove(Direction.RIGHT, moves=3, matrix=grid)
```

## License
MIT License