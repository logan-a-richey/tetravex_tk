# engine.py 

import random

class Block:
    def __init__(self, i, j):
        # block coordinates
        self.i = i
        self.j = j 
        
        # edge values
        self.n = 0
        self.e = 0
        self.s = 0
        self.w = 0

        self.enable = 0

class Engine:
    def __init__(self):
        self.gm = None 
        self.size = 3

    def new_game(self, size: int):
        self.size = size
        self.grid = [[Block(row, col) for col in range(size * 2)] for row in range(size) ]
        
        for i in range(size):
            for j in range(size):
                b = self.grid[i][j] 
                b.enable = 1

                b.n, b.e, b.s, b.w = [random.randint(0, 9) for _ in range(4) ]
                if (i > 0):
                    b2 = self.grid[i-1][j]
                    b.n = b2.s
                if (j > 0):
                    b2 = self.grid[i-1][j-1]
                    b.w = b2.e
        
    def make_move(self, i1, j1, i2, j2):
        # do swap
        b1 = self.grid[i1][j1]
        b2 = self.grid[i2][j2]
        b1, b2 = b2, b1
        
        self.gm.draw_canvas() 

    def is_win(self):
        for i in range(self.size):
            for j1 in range(self.size):
                j2 = j1 + self.size 
                
                b1 = self.grid[i][j2]

                # check north
                if (i > 0):
                    b2 = self.grid[i-1][j2]
                    if (b1.n != b2.s): return False 
                # check south
                if (i < self.size):
                    b2 = self.grid[i+1][j2] 
                    if (b1.s != b2.n): return False 

                # check east
                if (j < self.size * 2):
                    b2 = self.grid[i][j2+1]
                    if (b1.e != b2.w): return False

                # check west
                if (j > size.size):
                    b2 = self.grid[i][j2-1]
                    if (b1.w != b2.e): return False

        return True
        




