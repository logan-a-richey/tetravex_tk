# controller.py 

from dataclasses import dataclass 
from typing import List, Tuple, Optional

from model.engine import Engine, Move
from controller.settings_manager import SettingsManager
from view.main_window import MainWindow

@dataclass
class SquareState:
    clicked_square: Optional[Tuple[int, int]]
    bad_coords: List[Tuple[int, int]]
    hint_coords: List[Tuple[int, int]]


class Controller:
    def __init__(self, root):
        self.root = root 

        self.engine = Engine()
        self.settings_manager = SettingsManager()
        self.main_window = MainWindow(root, self)
        
        # game variables
        self.clicked_square = None
        self.bad_coords: List[Tuple[int, int]] = []
        self.hint_coords: List[Tuple[int, int]] = []
        
        self.current_board_state = self.engine.get_state()
        self.current_setting_state = self.settings_manager.get_state()
        
        self.last_size = 3
        self.seen_win = False

        # setup new game
        self.on_new_game(self.last_size)

    def on_new_game(self, size: int):
        self.clicked_square = None 
        self.bad_coords.clear()
        self.hint_coords.clear()
        self.seen_win = False
        
        self.engine.new_game(size)
        self.current_board_state = self.engine.get_state()
        self.current_setting_state = self.settings_manager.get_state()

        self.resize_window()
        self.refresh()
    
    def on_quit(self):
        print("[INFO] Quitting")
        self.root.quit()
    
    def get_mouse_coords(self, event) -> Optional[Tuple[int, int]]:
        self.current_board_state = self.engine.get_state()
        self.current_setting_state = self.settings_manager.get_state()

        size    = self.current_board_state.num_rows
        numRows = self.current_board_state.num_rows
        numCols = self.current_board_state.num_cols
        tile    = self.current_setting_state.tile_size
        margin  = self.current_setting_state.tile_size // 2

        i = event.y // tile

        # Determine column index with margin adjustment
        if event.x < size * tile:
            j = event.x // tile
        elif event.x < size * tile + margin:
            return
        else:
            j = (event.x - margin) // tile
        
        # bounds check
        if i < 0 or j < 0 or i >= numRows or j >= numCols:
            return
        
        coord = (i, j)
        return coord
    
    def on_make_move(self, i1, j1, i2, j2):
        my_move = Move(i1, j1, i2, j2)
        self.engine.make_move(my_move)
        self.clicked_square = None
        self.hint_coords.clear()
        
        self.refresh()

        self.check_for_win()

    def check_for_win(self):
        if self.seen_win:
            return
        
        res = self.engine.is_solved()
        if not res:
            return
        
        self.seen_win = True 
        self.main_window.win_popup.trigger()
    
    def on_click(self, event):
        coord = self.get_mouse_coords(event)
        print(coord)

        if not coord:
            self.clicked_square = None
            self.refresh()
            return
        if self.clicked_square:
            # make move (swap)
            self.on_make_move(
                coord[0], 
                coord[1], 
                self.clicked_square[0], 
                self.clicked_square[1]
            )
        else:
            self.clicked_square = coord
            self.refresh()
    
    def on_get_hint(self):
        print("hint")

        if self.hint_coords:
            self.on_make_move(
                self.hint_coords[0][0],
                self.hint_coords[0][1],
                self.hint_coords[1][0],
                self.hint_coords[1][1]
            )
        else:
            self.hint_coords = self.engine.get_hint_coords()
            self.refresh()
    
    def get_square_state(self):
        self.bad_coords = self.engine.get_wrong_coords()

        return SquareState(
            self.clicked_square,
            self.bad_coords,
            self.hint_coords
        )

    def refresh(self):
        #print("Controller::refresh() called")
        
        board_state = self.engine.get_state()
        settings_state = self.settings_manager.get_state() 
        square_state = self.get_square_state()
        
        print(square_state.hint_coords)

        self.main_window.canvas.redraw(
            board_state, 
            settings_state, 
            square_state
        )

    def on_zoom_out(self): 
        MIN_TILE_SIZE = 50
        ts = self.current_setting_state.tile_size 
        ts = max(MIN_TILE_SIZE, ts - 10)
        
        self.settings_manager.set_tile_size(ts)
        self.current_setting_state = self.settings_manager.get_state()
        self.resize_window()
        self.refresh()

    def on_zoom_in(self):
        MAX_TILE_SIZE = 200
        ts = self.current_setting_state.tile_size 
        ts = min(MAX_TILE_SIZE, ts + 10)
        
        self.settings_manager.set_tile_size(ts)
        self.current_setting_state = self.settings_manager.get_state()
        self.resize_window()
        self.refresh()

    def new_of_prev_size(self):
        self.new_game(self.last_size)

    def resize_window(self):
        num_rows = self.current_board_state.num_rows
        num_cols = self.current_board_state.num_cols
        ts = self.current_setting_state.tile_size 

        m = ts // 2
        w = num_cols * ts + m
        h = num_rows * ts

        self.root.geometry("{}x{}".format(w, h))

