"""
Array2D Library
===============

A lightweight library for 2D coordinate systems and grid-based data structures.

Coordinate System:
- Positive X goes right
- Positive Y goes down
- Origin (0,0) is top-left

Classes:
- Point: Represents a coordinate with optional data of any type
- Array2D: 2D grid of Points with fast lookup
- Direction: Enum for cardinal directions
"""

from __future__ import annotations
from enum import Enum
from typing import Tuple
from warnings import warn

class Direction(Enum):

    """Four cardinal directions. Should be self-explanatory."""
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

class Point:
    
    """Initialize Point"""
    def __init__(self, xyPair: Tuple[int,int], data=None) -> None:
        self._xyPair = xyPair
        self._data = data

    """Basic data for debugging"""
    def __repr__(self) -> str:
        return f'Point({self._xyPair}), data={self._data}'

    """Get data stored in Point"""
    def getData(self):
        return self._data
    
    """Update data stored in Point"""
    def setData(self, data) -> None:
        self._data = data

    """Return (x, y) coordinates of Point"""
    def getPos(self) -> Tuple[int, int]:
        return self._xyPair

    """Update exact (x, y) coordinates of Point"""
    def setPos(self, xyPair: Tuple[int,int], matrix: Array2D | None = None) -> None:
        if not matrix or matrix.cols > xyPair[0] and matrix.rows > xyPair[1] and xyPair[0] >= 0 and xyPair[1] >= 0:
            self._xyPair = xyPair
        else:
            warn("ERROR: New Point position is out of range of given matrix. Point was not moved.")

    """Give location of new relative Point in a certain direction a certain number of times"""
    def getMove(self, direction: Direction, moves=1) -> Tuple[int, int]:
        match direction:
            case Direction.UP:
                return (self._xyPair[0], self._xyPair[1] - moves)
            case Direction.DOWN:
                return (self._xyPair[0], self._xyPair[1] + moves)
            case Direction.LEFT:
                return (self._xyPair[0] - moves, self._xyPair[1])
            case Direction.RIGHT:
                return (self._xyPair[0] + moves, self._xyPair[1])
            case _:
                warn("ERROR: No direction specified. Returning specified Point location.")
                return self._xyPair
            
    """Move this point a certain direction a certain number of times"""
    def setMove(self, direction: Direction, moves=1, matrix: Array2D | None = None) -> None:
        match direction:
            case Direction.UP:
                if not matrix or (self._xyPair[1] - moves) >= 0:
                    if matrix and matrix.wrapY:
                        self._xyPair = (self._xyPair[0], (self._xyPair[1] - moves) % matrix.rows)
                    else:
                        self._xyPair = (self._xyPair[0], self._xyPair[1] - moves)
                else: warn("ERROR: New Point position is out of range of given matrix. Point was not moved.")
            case Direction.DOWN:
                if not matrix or (self._xyPair[1] + moves) < matrix.rows:
                    if matrix and matrix.wrapY:
                        self._xyPair = (self._xyPair[0], (self._xyPair[1] + moves) % matrix.rows)
                    else:
                        self._xyPair = (self._xyPair[0], self._xyPair[1] + moves)
                else: warn("ERROR: New Point position is out of range of given matrix. Point was not moved.")
            case Direction.LEFT:
                if not matrix or (self._xyPair[0] - moves) >= 0:
                    if matrix and matrix.wrapX:
                        self._xyPair = ((self._xyPair[0] - moves) % matrix.cols, self._xyPair[1])
                    else:
                        self._xyPair = (self._xyPair[0] - moves, self._xyPair[1])
                else: warn("ERROR: New Point position is out of range of given matrix. Point was not moved.")
            case Direction.RIGHT:
                if not matrix or (self._xyPair[0] + moves) < matrix.cols:
                    if matrix and matrix.wrapX:
                        self._xyPair = ((self._xyPair[0] + moves) % matrix.cols, self._xyPair[1])
                    else:
                        self._xyPair = (self._xyPair[0] + moves, self._xyPair[1])
                else: warn("ERROR: New Point position is out of range of given matrix. Point was not moved.")
            case _:
                warn("ERROR: No direction specified. Point was not moved.")

class Array2D:
    
    """Initialize 2D array with immutable Points, no gaps or overlap allowed"""
    def __init__(self, rows: int, cols: int, defaultData=None, wrapX = False, wrapY = False) -> None:
        self._rows = rows
        self._cols = cols
        self._wrapX = wrapX
        self._wrapY = wrapY
        self._matrix = {
            (j,i): Point((j,i),defaultData)
            for i in range(rows)
            for j in range(cols)
        }

    """Basic data for debugging"""
    def __repr__(self) -> str:
        return f'Array2D({self._rows}x{self._cols})'

    """Pull data from Point at given coordinates"""
    def getData(self, xyPair: Tuple[int,int]):
        try:
            return self._matrix[xyPair].getData()
        except KeyError:
            warn("ERROR: Given coordinates are out of range. Returning None.")
        return None

    """Update data from Point at given coordinates"""
    def setData(self, xyPair: Tuple[int,int], data) -> None:
        try:
            self._matrix[xyPair].setData(data)
        except KeyError:
            warn("ERROR: Given coordinates are out of range. No Point data was updated.")

    """Return all coordinates containing a specific piece of data"""
    def dataLocs(self, data) -> list[Tuple[int,int]]:
        dataList = []
        for key, value in self._matrix.items():
            if value.getData() == data: dataList.append(key)
        return dataList

    """Return number of rows in matrix"""
    @property
    def rows(self) -> int:
        return self._rows 

    """Return number of columns in matrix"""
    @property
    def cols(self) -> int:
        return self._cols
    
    """Returns whether matrix can wrap around for Point x-movement"""
    @property
    def wrapX(self) -> bool:
        return self._wrapX
    
    """Returns whether matrix can wrap around for Point y-movement"""
    @property
    def wrapY(self) -> bool:
        return self._wrapY


