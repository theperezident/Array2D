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
    
    def __init__(self, xyPair: Tuple[int,int], data=None) -> None:
        """Initialize Point with optional data storage"""

        self._xyPair = xyPair
        self._data = data

    def __repr__(self) -> str:
        """Basic data for debugging"""

        return f'Point({self._xyPair}), data={self._data}'

    def getData(self):
        """Get data stored in Point"""

        return self._data
    
    def setData(self, data) -> None:
        """Update data stored in Point"""

        self._data = data

    def loadFrom(self, matrix: Array2D) -> None:
        """Assign data from same located point on given matrix to this point"""

        self._data = matrix.getData(self._xyPair)

    def saveTo(self, matrix: Array2D) -> None:
        """Assign data from this point to same located point on given matrix"""

        matrix.setData(self._xyPair,self._data)

    def getPos(self) -> Tuple[int, int]:
        """Return (x, y) coordinates of Point"""

        return self._xyPair

    def setPos(self, xyPair: Tuple[int,int], matrix: Array2D | None = None) -> None:
        """Update exact (x, y) coordinates of Point"""

        if not matrix or matrix.cols > xyPair[0] and matrix.rows > xyPair[1] and xyPair[0] >= 0 and xyPair[1] >= 0:
            self._xyPair = xyPair
        else:
            warn("ERROR: New Point position is out of range of given matrix. Point was not moved.")

    def getMove(self, direction: Direction, moves=1) -> Tuple[int, int]:
        """Give location of new relative Point in a certain direction a certain number of times"""

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
            
    def setMove(self, direction: Direction, moves=1, matrix: Array2D | None = None) -> None:
        """Move this point a certain direction a certain number of times"""

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
    
    
    def __init__(self, cols: int, rows: int, defaultData=None, wrapX=False, wrapY=False) -> None:
        """Initialize 2D array with immutable coordinates, no gaps or overlap allowed"""
        
        if cols < 1 or rows < 1: raise Exception("Cannot initiate an Array2D with less than 1 row and/or column")

        try:
            self._rows = rows
            self._cols = cols
            self._wrapX = wrapX
            self._wrapY = wrapY
            self._matrix = {
                (i,j): defaultData
                for j in range(rows)
                for i in range(cols)
            }
        except Exception as e:
            print(f'ERROR: {e}')

    
    def __repr__(self) -> str:
        """Basic data for debugging"""

        return f'Array2D({self._rows}x{self._cols})'
    
    
    def __iter__(self):
        """Yields all dictionary entries of this Array2D as Points, iterates over rows (left to right, then down at end of row)"""

        for coord, data in self._matrix.items():
            yield Point(coord,data)
    
    
    def iterLocs(self, cols: None | int | list[int] = None, rows: None | int | list[int] = None, transpose: bool = False):
        """Yields the x, y tuple in row-iterating order for the given cols and rows, iterates over entire Array2D if cols/rows unspecified.
        No values iterates all points in Array2D. transpose = True iterates over columns instead of rows"""

        giveWarning = True

        if isinstance(cols, int): cols = [cols]
        if isinstance(rows, int): rows = [rows]

        if cols == None: cols = [i for i in range(self._cols)]
        if rows == None: rows = [i for i in range(self._rows)]

        if not (isinstance(cols, list) and isinstance(rows, list)):
            raise Exception("Invalid argument type, expected int or list of ints for cols and rows. No iterator function returned.")
        try:
            if not transpose:
                for j in rows:
                    for i in cols:
                        if i < self._cols and j < self._rows:
                            yield (i,j)
                        else:
                            if giveWarning: warn("ERROR: At least one listed row/column was out of range of the source matrix. Returning only coordinates within matrix bounds.")
                            giveWarning = False
            else:
                for i in cols:
                    for j in rows:
                        if i < self._cols and j < self._rows:
                            yield (i,j)
                        else:
                            if giveWarning: warn("ERROR: At least one listed row/column was out of range of the source matrix. Returning only coordinates within matrix bounds.")
                            giveWarning = False
        except Exception as e:
            print(f'ERROR: {e}')

    def getData(self, xyPair: Tuple[int,int] | list[Tuple[int,int]]):
        """Pull data from point at given coordinates. Returns list of data if list of tuple(x,y) provided. Returns None for coordinates out of range of array"""

        if isinstance(xyPair, tuple):
            try:
                return self._matrix[xyPair]
            except KeyError:
                warn("ERROR: Given coordinates are out of range. Returning None.")
                return None
        elif (isinstance(xyPair, list) and all(isinstance(p, tuple) and len(p) == 2 for p in xyPair)):
            dataList = []
            giveWarning = True
            for pair in xyPair:
                try:
                    dataList.append(self._matrix[pair])
                except KeyError:
                    dataList.append(None)
                    if giveWarning: warn("ERROR: At least one coordinate was out of range of matrix. Returning None for data of invalid coordinates.")
                    giveWarning = False
            return dataList
        else:
            warn("ERROR: Passed an invalid argument type, expected Tuple[int,int] or list of Tuple[int,int]. Returning None.")
            return None

    def setData(self, xyPair: Tuple[int,int] | list[Tuple[int,int]], data) -> None:
        """Update data for given coordinates"""
        
        giveWarning = False
        if isinstance(xyPair,tuple): xyPair = [xyPair]

        if not (isinstance(xyPair, list) and all(isinstance(p, tuple) and len(p) == 2 for p in xyPair)):
            raise Exception("ERROR: Passed an invalid argument type, expected Tuple[int,int] or list of Tuple[int,int]. No data updates completed")

        try:
            for coord in xyPair:
                if coord in self._matrix:
                    self._matrix[coord] = data
                else:
                    giveWarning = True
        except Exception as e:
            print(f'ERROR: {e}')
        
        if giveWarning: warn("ERROR: Some listed rows/columns were out of range of the target matrix. Updating data only for coordinates within matrix bounds.")

    def loadFrom(self, point: Point) -> None:
        """Assign data from a given point directly to same coordinates on the matrix"""

        try:
            self._matrix[point.getPos()] = point.getData()
        except KeyError:
            warn("ERROR: Given point is out of range of this matrix. Matrix data was not updated.")

    def saveTo(self, point: Point) -> None:
        """Assign data from a matrix point to another Point object with the same coordinates"""
        try:
            point.setData(self._matrix[point.getPos()])
        except KeyError:
            warn("ERROR: Given point is out of range of this matrix. Point data was not updated.")

    def findAny(self, *data) -> list[Tuple[int,int]]:
        """Return all coordinates containing specific piece(s) of data"""

        dataList = []
        for key, value in self._matrix.items():
            if value in data: dataList.append(key)
        return dataList
    
    def asPoint(self, xyPair: Tuple[int,int]) -> Point | None:
        """Returns the requested coordinates as a full Point class"""

        try:
            return Point(xyPair,self._matrix[xyPair])
        except KeyError:
            warn("ERROR: Given coordinates are out of range. Returning None.")
            return None

    @property
    def rows(self) -> int:
        """Return number of rows in matrix"""

        return self._rows 

    @property
    def cols(self) -> int:
        """Return number of columns in matrix"""

        return self._cols
    
    @property
    def wrapX(self) -> bool:
        """Returns whether matrix can wrap around for Point x-movement"""

        return self._wrapX
    
    @property
    def wrapY(self) -> bool:
        """Returns whether matrix can wrap around for Point y-movement"""
        
        return self._wrapY


