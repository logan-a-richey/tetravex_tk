# app.py

import tkinter as tk 

from engine import Engine
from theme_manager import ThemeManager

from typing import Optional, Tuple, List

class App:
    def __init__(self):
        # contains all of the game logic
        self.engine = Engine()  

        # settings
        self.theme_manager = ThemeManager() 
        self.enable_bad_rect = True

        # game variables
        self.last_size = 3
        self.tile_size = 100
        self.grid_margin = self.tile_size // 2
        self.seen_win = False 
        self.clicked_tile = None
        self.hint_tiles = []
        self.bad_tiles = [] 

        # finish tk setup 
        self.root = tk.Tk()
        self.root.title("Tetravex GUI App")
        self.setup_widgets()
        self.on_new_game(size=3)
    
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
        # bound check the size
        size = max(2, size)
        size = min(8 ,size)

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
    
    def on_prefs_popup(self) -> None:
        popup = tk.Toplevel(self.root)
        popup.title("Preferences Window")
        popup.geometry("400x400")

        # **************************************************
        
        tk.Label(popup, text="Color Theme").pack(pady=4)
        valid_choices = list(self.theme_manager.themes.keys())

        current_theme = self.theme_manager.get()
        radio_var = tk.StringVar(value=current_theme.name)
        def on_radio_change():
            print("on radio change")
            text = radio_var.get()
            self.theme_manager.set(text)
            self.on_canvas_draw()

        for choice in valid_choices:
            tk.Radiobutton(
                popup,
                text=choice,
                variable=radio_var,
                value=choice,
                command=on_radio_change,
            ).pack(pady=4)
       
        # **************************************************
        
        checkbox_var = tk.BooleanVar(value=self.enable_bad_rect) 
        def on_checkbox_change():
            print("on checkbox change")
            val = checkbox_var.get()
            self.enable_bad_rect = val
            self.on_canvas_draw()

        
        tk.Checkbutton(popup, text="Enable Bad Rect Outline", variable=checkbox_var, command=on_checkbox_change).pack(pady=20)

        # **************************************************
        
        tk.Button(popup, text="Okay", command=popup.destroy).pack(pady=5)
        
        self.center_popup(popup)

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

    def on_win_popup(self) -> None:
        popup = tk.Toplevel(self.root)
        popup.title("Game over")
        popup.geometry("200x200")

        msg = '\n'.join([ "You completed the puzzle!", "Congrats!" ])
        label = tk.Label(popup, text=msg).pack(pady=20)
        
        close_button = tk.Button(popup, text="Okay", command=popup.destroy).pack(pady=4)
        
        self.center_popup(popup)

    # --- Window Config Functions --- 
    def on_zoom_in(self):
        MAX_SIZE = 200
        self.tile_size = min(MAX_SIZE, self.tile_size + 10)
        self.resize_window()
        self.on_canvas_draw()
    
    def on_zoom_out(self):
        MIN_SIZE = 50
        self.tile_size = max(MIN_SIZE, self.tile_size - 10)
        self.resize_window()
        self.on_canvas_draw()

    def resize_window(self):
        screen_w = self.tile_size * self.engine.numCols + self.grid_margin * 2
        screen_h = self.tile_size * self.engine.numRows + self.grid_margin
        self.root.geometry("{}x{}".format(screen_w, screen_h) )

    # --- Canvas Functions --- 
    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="#707070")
        self.canvas.pack(side='top', fill='both', expand=True)
        
        self.canvas.bind('<Button-1>', lambda event: self.on_canvas_click(event) ) 
        self.root.bind('<Escape>', lambda event: self.on_quit() ) 
        
        self.root.bind('<Control-minus>', lambda event: self.on_zoom_out() )
        self.root.bind('<Control-equal>', lambda event: self.on_zoom_in() )
        
        self.root.bind('<Control-n>', lambda event: self.on_new_game(self.last_size) )
        self.root.bind('<Control-h>', lambda event: self.on_get_hint() )

        self.canvas.focus_set()
    
    def get_mouse_coordinates(self, event) -> Optional[Tuple[int, int]]:
        size = self.engine.numRows
        numRows = self.engine.numRows
        numCols = self.engine.numCols
        tile = self.tile_size
        margin = self.grid_margin

        i = event.y // tile

        # Determine column index with margin adjustment
        if event.x < size * tile:
            # left board
            j = event.x // tile
        elif event.x < size * tile + margin:
            # inside the margin → ignore click
            return
        else:
            # right board → subtract margin before computing j
            j = (event.x - margin) // tile
        
        # bounds check
        if i < 0 or j < 0 or i >= numRows or j >= numCols:
            return
        
        coord = (i, j)
        return coord

    def on_canvas_click(self, event):
        coord = self.get_mouse_coordinates(event)
        
        if self.clicked_tile:
            i1, j1, i2, j2 = coord[0], coord[1], self.clicked_tile[0], self.clicked_tile[1]

            self.engine.make_move(i1, j1, i2, i2)
            self.clicked_tile = None
        else:
            self.clicked_tile = coord

        self.on_canvas_draw()
        res = self.engine.is_solved()
        if res:
            self.on_win_popup()


    def get_font_color(self, hex_color) -> str:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        
        return "#ffffff" if luminance < 128 else "#000000"

    def dim_color(self, color) -> str:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)

        offset = 40 
        r = max(0, r - offset)
        g = max(0, g - offset)
        b = max(0, b - offset)

        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def draw_block(self, block, x0, y0, x1, y1, current_theme: "Theme", dimmed: bool):
        xc, yc = x0 + self.tile_size // 2, y0 + self.tile_size // 2
        b_c = (xc, yc)
        
        # vertices for tile
        b_nw, b_ne, b_sw, b_se = (x0, y0), (x1, y0), (x0, y1), (x1, y1)

        # text anchor positions
        tn = (x0 + int(self.tile_size * 0.50), y0 + int(self.tile_size * 0.25))
        te = (x0 + int(self.tile_size * 0.75), y0 + int(self.tile_size * 0.50))
        ts = (x0 + int(self.tile_size * 0.50), y0 + int(self.tile_size * 0.75))
        tw = (x0 + int(self.tile_size * 0.25), y0 + int(self.tile_size * 0.50))

        # Define edge data for looping
        edges = [block.n, block.e, block.s, block.w]
        triangles = [
            [b_c, b_ne, b_nw],  # N
            [b_c, b_se, b_ne],  # E
            [b_c, b_sw, b_se],  # S
            [b_c, b_nw, b_sw],  # W
        ]
        text_positions = [tn, te, ts, tw]

        # Draw each edge using a single loop
        for val, tri_pts, text_pos in zip(edges, triangles, text_positions):
            tri_color = current_theme.colors.get(val, '#000000')
            text_color = self.get_font_color(tri_color)
            if dimmed:
                tri_color = self.dim_color(tri_color)

            self.canvas.create_polygon(tri_pts, fill=tri_color, width=2, outline='#000000')
            self.canvas.create_text(
                *text_pos, 
                text=str(val), 
                anchor=tk.CENTER, 
                font=("Arial", int(self.tile_size * 0.15) ), 
                fill=text_color
            )
    
    def on_canvas_draw(self):
        self.canvas.delete("all")

        grid = self.engine.grid
        numRows = self.engine.numRows
        numCols = self.engine.numCols
        tile = self.tile_size
        current_theme = self.theme_manager.get()

        for i in range(numRows):
            for j in range(numCols):
                x0 = j * tile 
                y0 = i * tile 
                if j >= numCols // 2:
                    x0 += self.grid_margin
                x1 = x0 + tile
                y1 = y0 + tile
                
                # see if square has been clicked
                dimmed = False
                if self.clicked_tile:
                    if (i == self.clicked_tile[0] and j == self.clicked_tile[1]):
                        dimmed = True

                # draw grid
                bg_color = current_theme.colors.get('grid_bg', '#000000')
                if dimmed:
                    bg_color = self.dim_color(bg_color)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_color)
                
                # draw block
                block = grid[i][j] 
                if block.active:
                    self.draw_block(block, x0, y0, x1, y1, current_theme, dimmed)
                
                # draw bad rect
                if (i, j) in self.bad_tiles:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='', outline='#ff0000', width=4)
                
                # draw hint rect
                if (i, j) in self.hint_tiles:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='', outline='#00ff00', width=4)


    # --- Main functions ---
    def run(self):
        self.root.mainloop()
    
    def on_quit(self):
        self.root.quit()

