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
    
    def to_str(self):
        if self.enable:
            return '{}{}{}{}'.format(self.n, self.e, self.s, self.w)
        else:
            return "...."

class Engine:
    ''' Tetravex game logic '''
    def __init__(self):
        self.gm = None 
        self.size = 3

    def new_game(self, size: int):
        self.size = size
        self.grid = [[Block(row, col) for col in range(size * 2)] for row in range(size) ]
        
        blocks = []

        for i in range(size):
            for j in range(size):
                b = self.grid[i][j] 
                b.enable = 1

                b.n, b.e, b.s, b.w = [random.randint(0, 9) for _ in range(4) ]
                if (i > 0):
                    b2 = self.grid[i-1][j]
                    b.n = b2.s
                if (j > 0):
                    b2 = self.grid[i][j-1]
                    b.w = b2.e

                blocks.append(b)

        random.shuffle(blocks)
        for idx, block in enumerate(blocks):
            i = idx // self.size 
            j = idx % self.size
            self.grid[i][j] = block
        
    def make_move(self, i1, j1, i2, j2):
        # do swap
        self.grid[i1][j1], self.grid[i2][j2] = self.grid[i2][j2], self.grid[i1][j1]
    
    def print_playable(self):
        size = self.size
        offset = size
        for i in range(size):
            for j in range(offset, offset + size):
                print(self.grid[i][j].to_str(), end=' ')
            print()
    
    def get_wrong_coords(self):
        size = self.size
        offset = size  # playable region starts here
        wrong_coords = [] 

        for i in range(size):
            for j in range(offset, offset + size):
                b = self.grid[i][j]
                
                if not (b.enable):
                    continue

                # check west neighbor
                if j > offset:
                    left = self.grid[i][j - 1]
                    if b.w != left.e:
                        is_solved = 0 
                        wrong_coords.append( [i, j] )
                        continue

                # check east neighbor
                if j < offset + size - 1:
                    right = self.grid[i][j + 1]
                    if b.e != right.w:
                        wrong_coords.append( [i, j] )
                        continue

                # check north neighbor
                if i > 0:
                    top = self.grid[i - 1][j]
                    if b.n != top.s:
                        wrong_coords.append( [i, j] )
                        continue

                # check south neighbor
                if i < size - 1:
                    bottom = self.grid[i + 1][j]
                    if b.s != bottom.n:
                        wrong_coords.append( [i, j] )
                        continue

        return wrong_coords   

    def is_game_over(self):
        size = self.size
        offset = size  # playable region starts here

        for i in range(size):
            for j in range(offset, offset + size):
                b = self.grid[i][j]
                
                if not (b.enable):
                    return False 

                # check west neighbor
                if j > offset:
                    left = self.grid[i][j - 1]
                    if b.w != left.e: 
                        return False 

                # check east neighbor
                if j < offset + size - 1:
                    right = self.grid[i][j + 1]
                    if b.e != right.w:
                        return False 

                # check north neighbor
                if i > 0:
                    top = self.grid[i - 1][j]
                    if b.n != top.s:
                        return False 

                # check south neighbor
                if i < size - 1:
                    bottom = self.grid[i + 1][j]
                    if b.s != bottom.n:
                        return False 

        return True   
