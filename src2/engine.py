# engine.py 

from dataclasses import dataclass 
from typing import List, Tuple
import random 

@dataclass
class Block:
    i: int
    j: int
    ci: int
    ji: int
    n: int
    e: int
    s: int
    w: int
    active: bool

@dataclass 
class Move:
    i1: int
    j1: int
    i2: int
    j2: int

@dataclass 
class BoardState:
    num_rows: int
    num_cols: int
    grid: list

class Engine:
    def __init__(self):
        size = 3
        num_rows = size
        num_cols = size * 2

        self.grid = [[ Block(i, j, i, j + size, 0, 0, 0, 0, False) for j in range(num_cols)] for i in range(num_rows)]

    def new_game(self, size: int):
        num_rows = size
        num_cols = size * 2
        
        self.grid = [[ Block(i, j, i, j + size, 0, 0, 0, 0, False) for j in range(num_cols)] for i in range(num_rows)]

        blocks = []
        for i in range(size):
            for j in range(size):
                b = self.grid[i][j] 
                b.n, b.e, b.s, b.w = [random.randint(0, 9) for _ in range(4)]
                b.active = True
                
                if i > 0:
                    a = self.grid[i-1][j]
                    b.n = a.s
                if j > 0:
                    a = self.grid[i][j-1]
                    b.w = a.e
                
                blocks.append(b)

        random.shuffle(blocks)
        
        for idx, b in enumerate(blocks):
            i = idx // size 
            j = idx % size
            self.grid[i][j].i = i 
            self.grid[i][j].i = j
        
        self.print_grid()
    
    def block_say(self, b):
        if b.active:
            return "{}{}{}{}".format(b.n, b.e, b.s, b.w)
        else:
            return "...."
    
    def print_grid(self):
        for row in self.grid:
            for block in row:
                print(self.block_say(block), end=" ")
            print()

    def get_hint_coords(self):
        for row in self.grid:
            for block in row:
                if block.i != block.ci and block.j != block.cj:
                    return [ (i, j), (ci, cj) ]
        return []    

    def get_wrong_coords(self):
        wrong_coords = []
        
        directions = [ [-1, 0], [1, 0], [0, 1], [0, -1] ]
        block_attrs = ['n', 's', 'e', 'w']
        other_attrs = ['s', 'n', 'w', 'e']
        
        num_rows = len(self.grid)
        num_cols = len(self.grid[0])
        offset = num_cols // 2 
        
        # loop over grid on RHS
        for i in range(num_rows):
            for j in range(offset, num_cols):
                for direction, block_attr, other_attr in zip(directions, block_attrs, other_attrs):
                    if not self.grid[i][j].active:
                        continue

                    i2 = i + direction[0]
                    j2 = j + direction[1]
                    
                    if (i2 < 0 or i2 >= num_rows):
                        continue
                    if (j2 < offset or j2 >= num_cols):
                        continue

                    block_edge = getattr(self.grid[i][j], block_attr)
                    other_edge = getattr(self.grid[ci][cj], other_attr)

                    if (block_edge != other_edge):
                        wrong_coords.append(i, j)

        return wrong_coords 

    def is_solved(self) -> bool:
        directions = [ [-1, 0], [1, 0], [0, 1], [0, -1] ]
        block_attrs = ['n', 's', 'e', 'w']
        other_attrs = ['s', 'n', 'w', 'e']
        
        num_rows = len(self.grid)
        num_cols = len(self.grid[0])
        offset = num_cols // 2 
        
        # loop over grid on RHS
        for i in range(num_rows):
            for j in range(offset, num_cols):
                for direction, block_attr, other_attr in zip(directions, block_attrs, other_attrs):
                    if not self.grid[i][j].active:
                        return False

                    i2 = i + direction[0]
                    j2 = j + direction[1]
                    
                    if (i2 < 0 or i2 >= num_rows):
                        continue
                    if (j2 < offset or j2 >= num_cols):
                        continue

                    block_edge = getattr(self.grid[i][j], block_attr)
                    other_edge = getattr(self.grid[ci][cj], other_attr)

                    if (block_edge != other_edge):
                        return False

        return True
    
    def get_state(self) -> "BoardState":
        num_rows = len(self.grid)
        num_cols = len(self.grid[0])
        # hint_coords =
        # wrong_coords =
        return BoardState(num_rows, num_cols, self.grid)




