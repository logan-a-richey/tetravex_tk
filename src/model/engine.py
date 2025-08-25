# engine.py 

from dataclasses import dataclass 
from typing import List, Tuple
import random 

@dataclass
class Block:
    ci: int
    cj: int
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
    grid: List[List["Block"]]

class Engine:
    def __init__(self):
        size = 3
        num_rows = size
        num_cols = size * 2

        self.grid = [[ Block(i, j+size, 0, 0, 0, 0, False) for j in range(num_cols)] for i in range(num_rows)]

    def new_game(self, size: int):
        num_rows = size
        num_cols = size * 2
        
        self.grid = [[ Block(i, j + size, 0, 0, 0, 0, False) for j in range(num_cols)] for i in range(num_rows)]

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
            self.grid[i][j] = b
        
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
    
    def make_move(self, move: "Move"):
        i1, j1, i2, j2 = move.i1, move.j1, move.i2, move.j2  
        self.grid[i1][j1], self.grid[i2][j2] = self.grid[i2][j2], self.grid[i1][j1] 

    def get_hint_coords(self) -> List[Tuple[int, int]]:
        current_board_state = self.get_state()
        num_rows = current_board_state.num_rows
        num_cols = current_board_state.num_cols 
        
        for i, row in enumerate(self.grid):
            for j, b in enumerate(row):
                if b.active and (i != b.ci or j != b.cj):
                    # find the block currently at (b.ci, b.cj)
                    target = self.grid[b.ci][b.cj]
                    return [(i, j), (b.ci, b.cj)]
        return []
        
    def get_wrong_coords(self) -> List[Tuple[int, int]]:
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
                    
                    if not self.grid[i2][j2].active:
                        continue

                    block_edge = getattr(self.grid[i][j], block_attr)
                    other_edge = getattr(self.grid[i2][j2], other_attr)
                    
                    if (block_edge != other_edge):
                        coord = (i, j)
                        wrong_coords.append(coord)

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
                    other_edge = getattr(self.grid[i2][j2], other_attr)

                    if (block_edge != other_edge):
                        return False

        return True
    
    def get_state(self) -> "BoardState":
        num_rows = len(self.grid)
        num_cols = len(self.grid[0])
        # hint_coords =
        # wrong_coords =
        return BoardState(num_rows, num_cols, self.grid)

