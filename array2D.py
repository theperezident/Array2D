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
- Array2D: 2D grid of coordinates and data with fast lookup
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

    """Assign data from same located point on given matrix to this point"""
    def loadFrom(self, matrix: Array2D) -> None:
        self._data = matrix.getData(self._xyPair)

    """Assign data from this point to same located point on given matrix"""
    def saveTo(self, matrix: Array2D) -> None:
        matrix.setData(self._xyPair,self._data)

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
    
    """Initialize 2D array with immutable coordinates, no gaps or overlap allowed"""
    def __init__(self, cols: int, rows: int, defaultData=None, wrapX=False, wrapY=False) -> None:
        self._rows = rows
        self._cols = cols
        self._wrapX = wrapX
        self._wrapY = wrapY
        self._matrix = {
            (j,i): defaultData
            for j in range(cols)
            for i in range(rows)
        }

    """Basic data for debugging"""
    def __repr__(self) -> str:
        return f'Array2D({self._rows}x{self._cols})'
    
    """Yields the x, y tuple in row-iterating order for the given cols and rows, iterates over entire Array2D if cols/rows unspecified."""
    """No values iterates all points in Array2D. transpose = True iterates over columns instead of rows"""
    def iterLocs(self, cols: None | int | list[int] = None, rows: None | int | list[int] = None, transpose: bool = False):
        giveWarning = False

        if isinstance(cols, int): cols = [cols]
        if isinstance(rows, int): rows = [rows]

        if cols == None: cols = [i for i in range(self._cols)]
        if rows == None: rows = [i for i in range(self._rows)]

        assert isinstance(cols, list) and isinstance(rows, list)

        if not transpose:
            for j in rows:
                for i in cols:
                    if i < self._cols and j < self._rows:
                        yield (i,j)
                    else:
                        giveWarning = True
        else:
            for i in cols:
                for j in rows:
                    if i < self._cols and j < self._rows:
                        yield (i,j)
                    else:
                        giveWarning = True

        if giveWarning: warn("ERROR: Some listed rows/columns were out of range of the source matrix. Returned only coordinates within matrix bounds.")

    """Pull data from point at given coordinates. Returns list of data if list of tuple(x,y) provided. Returns None for coordinates out of range of array"""
    def getData(self, xyPair: Tuple[int,int] | list[Tuple[int,int]]):

        if isinstance(xyPair, tuple):
            try:
                return self._matrix[xyPair]
            except KeyError:
                warn("ERROR: Given coordinates are out of range. Returning None.")
                return None
        elif isinstance(xyPair, list):
            dataList = []
            giveWarning = False
            for pair in xyPair:
                try:
                    dataList.append(self._matrix[pair])
                except KeyError:
                    dataList.append(None)
                    giveWarning = True
            if giveWarning: warn("ERROR: At least one coordinate was out of range of matrix. Returned None for data of invalid coordinates.")
            return dataList
        else:
            warn("ERROR: Passed an invalid argument type. Returning None.")
            return None

    """Update data for given coordinates"""
    def setData(self, xyPair: Tuple[int,int] | list[Tuple[int,int]], data) -> None:
        
        giveWarning = False
        if isinstance(xyPair,tuple): xyPair = [xyPair]

        for coord in xyPair:
            if coord in self._matrix:
                self._matrix[coord] = data
            else:
                giveWarning = True
        
        if giveWarning: warn("ERROR: Some listed rows/columns were out of range of the target matrix. Updating data only for coordinates within matrix bounds.")

    """Assign data from a given point directly to same coordinates on the matrix"""
    def loadFrom(self, point: Point) -> None:
        try:
            self._matrix[point.getPos()] = point.getData()
        except KeyError:
            warn("ERROR: Given point is out of range of this matrix. Matrix data was not updated.")

    """Assign data from a matrix point to another Point object with the same coordinates"""
    def saveTo(self, point: Point) -> None:
        try:
            point.setData(self._matrix[point.getPos()])
        except KeyError:
            warn("ERROR: Given point is out of range of this matrix. Point data was not updated.")

    """Return all coordinates containing specific piece(s) of data"""
    def findAny(self, *data) -> list[Tuple[int,int]]:
        dataList = []
        for key, value in self._matrix.items():
            if value in data: dataList.append(key)
        return dataList
    
    """Returns the requested coordinates as a full Point class"""
    def asPoint(self, xyPair: Tuple[int,int]) -> Point | None:
        try:
            return Point(xyPair,self._matrix[xyPair])
        except KeyError:
            warn("ERROR: Given coordinates are out of range. Returning None.")
            return None

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


