# app.py

import tkinter as tk 

from engine import Engine
from ui.theme_manager import ThemeManager
from ui.popups import *
from ui.my_canvas import MyCanvas 

from typing import Optional, Tuple, List

class App:
    def __init__(self):
        # contains all of the game logic
        self.engine = Engine()  

        # settings
        self.theme_manager = ThemeManager() 
        self.enable_bad_rect = True
        self.last_size: int = 3
        self.seen_win: bool = False 

        # finish tk setup 
        self.root = tk.Tk()
        self.root.title("Tetravex GUI App")
        
        self.setup_menubar()
        self.my_canvas = MyCanvas(self)
        self.prefs_popup = PrefsPopup(self)
        self.about_popup = AboutPopup(self)
        self.win_popup = WinPopup(self)

        self.on_new_game(size=3)
    
    # --- Popup Functions --- 
    def on_prefs_popup(self) -> None:
        self.prefs_popup.open_popup()

    def on_about_popup(self) -> None:
        self.about_popup.open_popup()

    def on_win_popup(self) -> None:
        self.win_popup.open_popup()
    
    # --- Window config ---
    def resize_window(self):
        tile_size = self.my_canvas.tile_size
        margin = self.my_canvas.grid_margin
        numRows = self.engine.numRows
        numCols = self.engine.numCols

        screen_w = tile_size * numCols + margin * 2
        screen_h = tile_size * numRows + margin
        self.root.geometry("{}x{}".format(screen_w, screen_h) )
        self.on_canvas_draw()
    
    def setup_menubar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # --- File Menu ---
        file_menu = tk.Menu(menubar, tearoff=0)
        MAX_PUZZLE_SIZE = 8
        for i in range(2, MAX_PUZZLE_SIZE + 1):
            file_menu.add_command(label="{}x{}".format(i, i), command=lambda size=i: self.on_new_game(size) )

        file_menu.add_separator()
        
        file_menu.add_command(label="Quit", command=lambda: self.on_quit() )
        menubar.add_cascade(label="File", menu=file_menu) 
        
        # --- Prefs Menu ---
        prefs_menu = tk.Menu(menubar, tearoff=0)
        prefs_menu.add_command(label="Open Prefs", command=self.on_prefs_popup)
        menubar.add_cascade(label="Prefs", menu=prefs_menu)

        # --- About Menu ---
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Open About", command=self.on_about_popup)
        menubar.add_cascade(label="About", menu=about_menu)

    # --- Game Event Functions ---
    def on_new_game(self, size=3):
        # bound check the size
        size = max(2, size)
        size = min(8, size)

        # set game vars
        self.last_size = size 
        self.seen_win = False

        # call methods
        self.engine.new_grid(self.last_size)
        self.resize_window()
        self.on_canvas_draw()
    
    def on_canvas_draw(self):
        self.my_canvas.on_canvas_draw()
    
    def on_win(self):
        if self.seen_win:
            return
        self.seen_win = True
        self.on_win_popup()
    
    # --- Main functions ---
    def run(self):
        self.root.mainloop()
    
    def on_quit(self):
        self.root.quit()

