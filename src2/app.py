# app.py

import tkinter as tk 

from engine import Engine
from theme_manager import ThemeManager

from typing import Optional, Tuple, List

class App:
    def __init__(self):
        self.root = tk.Tk()     # tkinter gui
        self.root.title = "Tetravex GUI App"

        self.engine = Engine()  # contains all of the game logic
        self.theme_manager = ThemeManager() 

        # game variables
        self.last_size = 3
        self.tile_size = 100
        self.grid_margin = self.tile_size // 2
        self.seen_win = False 
        
        self.current_theme = self.theme_manager.get_default_theme()
        self.enable_bad_rect = True

        self.setup_widgets()
        self.on_new_game()
    
    # --- Init Widgets ---
    def setup_widgets(self):
        self.setup_menubar()
        self.setup_canvas()
    
    def setup_menubar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # --- File Menu ---
        file_menu = tk.Menu(menubar, tearoff=0)
        MAX_PUZZLE_SIZE = 8
        for i in range(2, MAX_PUZZLE_SIZE + 1):
            file_menu.add_command(label="{}x{}".format(i, i), command=lambda size=i: self.on_new_game(size) )

        file_menu.add_separator()
        
        # TODO 
        # file_menu.add_command(label="New Game", command=lambda: self.on_new_game(self.last_size))
        # file_menu.add_command(label="Get Hint", command=lambda: self.on_get_hint() )

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
    def on_get_hint(self):
        self.hint_coords = self.engine.get_hint_coords() 
        self.on_canvas_draw()

    def on_new_game(self, size=3):
        # set game vars
        self.last_size = size 
        self.seen_win = False

        # call methods
        self.engine.new_grid(self.last_size)
        self.resize_window()
        self.on_canvas_draw()
    
    def on_win(self):
        if self.seen_win:
            return
        self.seen_win = True
        self.on_win_popup()
    
    # --- Popup Functions --- 
    def center_popup(self, popup) -> None:
        popup.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry("+{}+{}".format(x, y))

    def on_about_popup(self) -> None:
        popup = tk.Toplevel(self.root)
        popup.title("About")
        popup.geometry("500x400")

        label_1 = tk.Label(popup, text="How to play", bg='#777777', font=("Arial", 16))
        label_1.pack(pady=4)

        msg = '\n'.join([
            'This is a clone of the game Tetravex',
            'Click 2 coordinates to swap blocks.',
            'The goal is to move all of the blocks from the left grid to the right grid,',
            'such that all adjacent edges are matching in value.',
            'Try to do it in as few moves possible!'
        ])

        label_2 = tk.Label(popup, text=msg)
        label_2.pack(pady=4)

        label_3 = tk.Label(popup, text="Controls", bg='#777777', font=("Arial", 16))
        label_3.pack(pady=4)

        msg = '\n'.join([
            'CTRL N : New game',
            'CTRL H : Get hint',
            'CTRL - : Zoom out',
            'CTRL = : Zoom in',
            'ESCAPE : Quit program'
        ])
        label_4 = tk.Label(popup, text=msg, font="TkFixedFont", anchor="w", justify="left")
        label_4.pack(pady=4)

        close_button = tk.Button(popup, text="Okay", command=popup.destroy)
        close_button.pack(pady=20)
        
        self.center_popup(popup)
    
    # TODO
    def on_prefs_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Preferences Window")
        popup.geometry("400x400")

        # --- Radio Widget ---
        tk.Label(popup, text="Color Theme:").pack(pady=5)
         
        valid_choices = list(self.theme_manager.themes.keys())
        radvar = tk.StringVar(value=self.current_theme)
    
        def on_radio_change():
            text = radvar.get()
            self.current_theme = text 
            print("on radio change: {}".format(text)) 
            self.on_canvas_draw()
            return 

        for choice in valid_choices:
            tk.Radiobutton( popup, text=choice, variable=radvar, value=choice, command=on_radio_change).pack(pady=4)

        # --- Checkbox widget ---- 
        checkbox_var = tk.BooleanVar(value=getattr(self, "show_wrong_tile", False))

        def on_checkbox_change():
            var = checkbox_var.get()
            print("on checkbox change: {}".format(var))
            self.enable_bad_rect = var
            self.on_canvas_draw()
            return 

        tk.Checkbutton( popup, text="Show wrong tile outline", variable=checkbox_var, command=on_checkbox_change).pack(pady=20)

        # --- Okay button ---
        tk.Button(popup, text="Okay", command=popup.destroy).pack(pady=5)
        
        self.center_popup(popup)
    
    def on_win_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Game over")
        popup.geometry("300x300")

        msg = '\n'.join([
            "You completed the puzzle!",
            "Congrats!"
        ])

        label = tk.Label(popup, text=msg)
        label.pack(pady=20)
        
        close_button = tk.Button(popup, text="Okay", command=popup.destroy)
        close_button.pack()

        self.center_popup(popup)

    # --- Window Config Functions --- 
    def on_zoom_in(self):
        MAX_SIZE = 200
        self.tile_size = min(MAX_SIZE, self.tile_size + 10)
        self.resize_window()
        self.draw()
    
    def on_zoom_out(self):
        MIN_SIZE = 50
        self.tile_size = max(MIN_SIZE, self.tile_size - 10)
        self.resize_window()
        self.draw()

    def resize_window(self):
        screen_w = self.tile_size * self.engine.numCols + self.grid_margin * 2
        screen_h = self.tile_size * self.engine.numRows + self.grid_margin
        self.root.geometry("{}x{}".format(screen_w, screen_h) )

    # --- Canvas Functions --- 
    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="#707070")
        self.canvas.pack(side='top', fill='both', expand=True)
        
        self.canvas.bind('<Button-1>', lambda event: self.on_button1_event(event) ) 
        self.root.bind('<Escape>', lambda event: self.on_quit() ) 
        
        self.root.bind('<Control-minus>', lambda event: self.on_zoom_out() )
        self.root.bind('<Control-equal>', lambda event: self.on_zoom_in() )
        
        self.root.bind('<Control-n>', lambda event: self.on_new_game(self.last_size) )
        self.root.bind('<Control-h>', lambda event: self.on_get_hint() )

        self.canvas.focus_set()
    
    def get_mouse_coordinates(self, event) -> Optional[Tuple[int, int]]:
        return

    def on_canvas_click(self, event):
        coords = self.get_mouse_coordinates()
    
    def draw_block(self):
        pass 
    
    # TODO 
    def on_canvas_draw(self):
        self.canvas.delete("all")

        for i in range(self.engine.numRows):
            for j in range(self.engine.numCols):
                b = self.engine.grid[i][j] 
                pass
        pass 
    
    # --- Main functions ---
    def run(self):
        self.root.mainloop()
    
    def on_quit(self):
        self.root.quit()

