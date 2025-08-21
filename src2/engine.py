# engine.py

import random 
from typing import List, Tuple, Optional

class Block:
    def __init__(self, i, j):
        self.i, self.j = i, j
        self.n, self.e, self.s, self.w = 0, 0, 0, 0
        self.ci = 0
        self.cj = 0
        self.active = False 

    def to_str(self):
        if self.active:
            return "{}{}{}{}".format(self.n, self.e, self.s, self.w)
        else:
            return "...."

class Engine:
    def __init__(self):
        self.numRows = 3 
        self.numCols = 6 
        self.grid: Optional[List[List["Block"]]] = None

    def new_grid(self, size: int) -> None:
        self.numRows = size 
        self.numCols = size * 2 
        self.grid = [[Block(i, j) for j in range(self.numCols)] for i in range(self.numRows)]
        blocks = []
        for i in range(size):
            for j in range(size):
                b = self.grid[i][j]
                b.active = True
                b.n, b.e, b.s, b.w = [random.randint(0, 9) for _ in range(4)]
                b.ci = i
                b.cj = j + size
                # bounds check - set matching edges
                if (i > 0):
                    a = self.grid[i-1][j]
                    b.n = a.s 
                if (j > 0):
                    a = self.grid[i][j-1]
                    b.w = a.e 
                blocks.append(b)
        random.shuffle(blocks)
        for idx, b in enumerate(blocks):
            i = idx // size
            j = idx % size 
            b.i, b.j = i, j
            self.grid[i][j] = b 
        return 

    def print_grid(self):
        for i in range(self.numRows):
            for j in range(self.numCols):
                b = self.grid[i][j] 
                print(b.to_str(), end=" ")
            print()
        return 

    def make_move(self, i1: int, j1: int, i2: int, j2: int) -> None:
        # bounds check
        if (i1 < 0 or i2 < 0 or i1 >= self.numRows or i2 >= self.numRows):
            return 
        if (j1 < 0 or j2 < 0 or j1 >= self.numCols or j2 >= self.numCols):
            return 
        b1 = self.grid[i1][j1]
        b2 = self.grid[i2][j2] 
        # swap references
        b1, b2 = b2, b1 
        # set references 
        b1.i, b2.j = i1, j1
        b2.i, b2.j = i2, j2
        return

    def get_wrong_coords(self) -> List[Tuple[int, int]]:
        wrong_coords = []
        offset = self.numRows 
        directions = [ [-1, 0], [1, 0], [0, 1], [0, -1] ]
        block_dirs = ['n', 's', 'e', 'w']
        other_dirs = ['s', 'n', 'w', 'e']
        for i in range(self.numRows):
            for j in range(offset, self.numCols):
                block = self.grid[i][j]
                if not block.active:
                    continue
                for direction, block_dir, other_dir in zip(directions, block_dirs, other_dirs):
                    i2 = i + direction[0] 
                    j2 = j + direction[1]
                    # bounds check
                    if (i2 < 0 or i2 >= self.numRows):
                        continue
                    if (j2 < offset or j2 >= self.numCols):
                        continue
                    other = self.grid[i2][j2]
                    block_val = getattr(block, block_dir)
                    other_val = getattr(other, other_dir)
                    if (block_val != other_val):
                        wrong_coords.append( (i, j) )
                        break
        return wrong_coords

    def is_solved(self) -> bool:
        offset = self.numRows 
        directions = [ [-1, 0], [1, 0], [0, 1], [0, -1] ]
        block_dirs = ['n', 's', 'e', 'w']
        other_dirs = ['s', 'n', 'w', 'e']
        for i in range(self.numRows):
            for j in range(offset, self.numCols):
                block = self.grid[i][j]
                if not block.active:
                    return False
                for direction, block_dir, other_dir in zip(directions, block_dirs, other_dirs):
                    i2 = i + direction[0] 
                    j2 = j + direction[1]
                    # bounds check
                    if (i2 < 0 or i2 >= self.numRows):
                        continue
                    if (j2 < offset or j2 >= self.numCols):
                        continue
                    other = self.grid[i2][j2]
                    block_val = getattr(block, block_dir)
                    other_val = getattr(other, other_dir)
                    if (block_val != other_val):
                        return False
        return True 
    
