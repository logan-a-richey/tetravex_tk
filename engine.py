# engine.py 

import random

class Block:
    def __init__(self):
        # block coordinates
        self.i = i
        self.j = j 
        
        # edge values
        self.n = 0
        self.e = 0
        self.s = 0
        self.w = 0


class Engine:
    def __init__(self):
        self.gm = None 
    
    def new_game(self, size:int):
        self.grid = []
