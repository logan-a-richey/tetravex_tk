# engine.py

from dataclasses import dataclass
from typing import List, Tuple, Optional, Callable
import random 

@dataclass
class Block:
    n: int
    e: int
    s: int
    w: int
    i: int 
    j: int
    ci: int
    cj: int
    active: bool

@dataclass 
class Move:
    i1: int 
    i2: int 
    j1: int 
    j2: int 

class Engine:
    def __init__(self):
        self.numRows = 3
        self.numCols = 6
        self.grid = []
        self.move_history = [] 
        self.move_history_idx = 0 

    def new_game(self, size: int):
        self.move_history.clear()
        self.move_history_idx = 0 

        self.numRows = size 
        self.numCols = size * 2

        self.grid = [[Block(0, 0, 0, 0, i, j, i, j + size, False) for j in range(self.numCols)] for i in range(self.numRows)]
        
        blocks = []
        
        for i in range(size):
            for j in range(size):
                b = self.grid[i][j]
                b.active = True
                b.n, b.e, b.s, b.w = [random.randint(0, 9) for _ in range(4)]
                if (i > 0):
                    a = self.grid[i-1][j]
                    b.n = a.s 
                if (j > 0):
                    a = self.grid[i][j-1]
                    b.w = a.e 
                blocks.append(b)

        print("before")
        self.print_board() 

        random.shuffle(blocks)

        print("after")
        self.print_board() 
        
        for idx, b in enumerate(blocks):
            i = idx // size 
            j = idx % size 
            self.grid[i][j] = b
            self.grid[i][j].i = i 
            self.grid[i][j].j = j 
    
    def block_to_str(self, b: Block) -> str:
        if b.active:
            return "{}{}{}{}".format(b.n, b.e, b.s, b.w)
        else:
            return "...."

    def print_board(self):
        for i in range(self.numRows):
            for j in range(self.numCols):
                b = self.grid[i][j] 
                b_str = self.block_to_str(b)
                print(b_str, end=" ")
            print()

    def make_move(self, move: Move, trunc=True):
        i1 = move.i1 
        j1 = move.j1
        i2 = move.i2 
        j2 = move.j2

        if (i1 < 0 or i1 >= self.numRows):
            print("[E] i1 out of range")
            return 
        if (i2 < 0 or i2 >= self.numRows):
            print("[E] i2 out of range")
            return 
        if (j1 < 0 or j1 >= self.numCols):
            print("[E] j1 out of range")
            return 
        if (j2 < 0 or j2 >= self.numCols):
            print("[E] j2 out of range")
            return 
        
        # swap blocks
        self.grid[i1][j1], self.grid[i2][j2] = self.grid[i2][j2], self.grid[i1][j1] 
        self.grid[i1][j1].i = i1 
        self.grid[i1][j1].j = j1 
        self.grid[i2][j2].i = i2 
        self.grid[i2][j2].j = j2 

        if trunc:
            next_idx = self.move_history_idx + 1
            del self.move_history_idx[next_idx:]
        
        self.move_history.append(move)
        self.move_history_idx += 1

    def undo_move(self):
        prev_idx = self.move_history_idx
        if prev_idx <= 0:
            return 
        
        last_move: Move = self.move_history[prev_idx]
        self.make_move(last_move, trunc=False)
        self.move_history_idx -= 1

    def redo_move(self):
        next_idx = self.move_history + 1
        if next_idx + 1 >= len(self.move_history):
            return 

        next_move = self.move_history[next_idx]
        self.make_move(next_move, trunc=False)
        self.move_history_idx += 1 

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
                    if (not other.active):
                        continue

                    block_val = getattr(block, block_dir)
                    other_val = getattr(other, other_dir)
                    if (block_val != other_val):
                        wrong_coords.append( (i, j) )
                        break

        return wrong_coords
    
    def get_hint_coords(self) -> List[Tuple[int, int]]:
        for i in range(self.numRows):
            for j in range(self.numCols):
                b = self.grid[i][j] 
                if not b.active:
                    continue
                correct = (b.i == b.ci and b.j == b.cj)
                if not correct:
                    hint_coords = [ (b.i, b.j), (b.ci, b.cj) ]
                    return hint_coords 
        return []

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
