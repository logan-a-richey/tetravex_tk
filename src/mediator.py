import tkinter as tk 

from typing import Optional, Tuple

from engine import Engine, Move
from ui.app import App
from ui.theme_manager import ThemeManager 

class Mediator:
    def __init__(self, root):
        # game logic
        self.engine = Engine()
        
        # game settings
        self.theme_manager = ThemeManager()
        self.enable_bad_rect = True

        # game variables
        self.clicked_tile = None 
        self.wrong_coords = []
        self.hint_coords = [] 
        self.hints_used = 0 
        self.last_size = 3
        
        # game gui
        self.app = App(root, self)

        # launch game
        self.handle_new_game(size=self.last_size)

    def refresh(self):
        self.app.canvas.refresh(
            self.engine.grid,
            self.clicked_tile,
            self.wrong_coords,
            self.hint_coords,
            self.enable_bad_rect
        )
    
    def get_coords(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        size = self.engine.numRows
        numRows = self.engine.numRows
        numCols = self.engine.numCols

        # TODO 
        my_canvas = self.app.canvas 
        tile = my_canvas.tile_size
        margin = my_canvas.grid_margin

        i = y // tile

        # Determine column index with margin adjustment
        if x < size * tile:
            j = x // tile # left board
        elif x < size * tile + margin:
            return # inside margin (ignore)
        else:
            j = (x - margin) // tile # right board
        
        # bounds check
        if i < 0 or j < 0 or i >= numRows or j >= numCols:
            return
        
        coord = (i, j)
        return coord
    
    def handle_click(self, x: int, y: int):
        coord = self.get_coords(x, y)
        if not coord:
            self.clicked_tile = None
            self.refresh()
            return 
        
        if coord:
            move = Move(coord[0], coord[1], self.clicked_tile[0], self.clicked_tile[1])
            self.engine.make_move(move)
            self.clicked_tile = None
        else:
            self.clicked_tile = coord    
        self.refresh()

    def handle_hint(self):
        print("in handle_hint")
#        if self.hint_tiles:
#            i1 = self.hint_tiles[0][0] 
#            j1 = self.hint_tiles[0][1]
#            i2 = self.hint_tiles[1][0]
#            j2 = self.hint_tiles[1][1] 
#            self.on_make_move(i1, j1, i2, j2)
#            
#            self.hint_tiles.clear() 
#        else:
#            self.hint_tiles = self.engine.get_hint_coords() 
        self.refresh()

    def handle_undo(self):
        print("in handle_undo")
        self.engine.undo_move()
        self.app.canvas.draw() 

    def handle_redo(self):
        print("in handle_redo")
        self.engine.redo_move()
        self.app.canvas.draw()

    def handle_new_game(self, size=None):
        print("handle_new_game({})".format(size))
        if not size:
            size = self.last_size 
        
        self.clicked_tile = None
        self.wrong_coords.clear()
        self.hint_coords.clear() 
        self.hints_used  = 0

        self.engine.new_game(size)

        self.refresh()
