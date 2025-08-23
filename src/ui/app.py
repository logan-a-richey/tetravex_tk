# app.py

import tkinter as tk 

from ui.popups import *
from ui.my_canvas import MyCanvas 

class App(tk.Frame):
    def __init__(self, root, mediator):
        super().__init__(root)
        self.root = root
        self.mediator = mediator
        
        self.pack()
        
        self.canvas = MyCanvas(
            root,
            mediator.handle_click,
            mediator.theme_manager
        )

        self.prefs_popup = PrefsPopup(
            root,
            mediator.theme_manager, 
            mediator.enable_bad_rect,
            mediator.refresh
        )

        self.about_popup = AboutPopup(root)
        self.win_popup = WinPopup(root)
        
        self.root.bind('<Control-minus>', lambda event: self.on_zoom_out() )
        self.root.bind('<Control-equal>', lambda event: self.on_zoom_in() )
        self.root.bind('<Escape>', lambda event: self.root.quit() ) 

        # TODO 
        # self.root.bind('<Control-n>', lambda event: self.app.on_new_game(self.app.last_size) )
        # self.root.bind('<Control-h>', lambda event: self.on_get_hint() )
        
        self.setup_menubar()

    # --- Window config ---
    def resize_window(self, w, h):
        self.root.geometry("{}x{}".format(w, h) )
        self.refresh()
    
    def on_zoom_in(self):
        MAX_SIZE = 200
        self.tile_size = min(MAX_SIZE, self.tile_size + 10)
        self.resize_window()
    
    def on_zoom_out(self):
        MIN_SIZE = 50
        self.tile_size = max(MIN_SIZE, self.tile_size - 10)
        self.resize_window()

    # --- Menubar ---  
    def setup_menubar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # --- File Menu ---
        file_menu = tk.Menu(menubar, tearoff=0)
        MAX_PUZZLE_SIZE = 8
        for i in range(2, MAX_PUZZLE_SIZE + 1):
            msg = "New {}x{} Puzzle".format(i, i)
            file_menu.add_command(label=msg, command=lambda size=i: self.mediator.handle_new_game(size=size))
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=lambda: self.root.quit() )
        menubar.add_cascade(label="File", menu=file_menu) 

        # --- Game Menu ---
        game_menu = tk.Menu(menubar, tearoff=0) 
        game_menu.add_command(label="Get Hint", command=self.mediator.handle_hint)
        game_menu.add_command(label="Undo Move", command=self.mediator.handle_undo)
        game_menu.add_command(label="Redo Move", command=self.mediator.handle_redo)
        menubar.add_cascade(label="Game", menu=game_menu)

        # --- Prefs Menu ---
        prefs_menu = tk.Menu(menubar, tearoff=0)
        prefs_menu.add_command(label="Open Prefs", command=self.prefs_popup.open_popup)
        menubar.add_cascade(label="Prefs", menu=prefs_menu)

        # --- About Menu ---
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Open About", command=self.about_popup.open_popup)
        menubar.add_cascade(label="About", menu=about_menu)
    