# app.py 

import tkinter as tk 
from tkinter import ttk 
from colors import Colors 

# globals
MIN_TILE_SIZE = 30
MAX_TILE_SIZE = 150
BOARD_MARGIN = 20  # width of gap between boards

class App:
    def __init__(self):
        self.gm = None 
        self.colors = Colors()
        
        self.color_map: dict = self.colors.get_color(0)
        
        self.show_wrong_tile: bool = False
        
        self.clicked_square = None 
        self.seen_game_over = 0 

    def finish_init(self):
        self.root = tk.Tk()
        self.screen_width, self.screen_height = (800, 600)
        self.root.geometry("{}x{}".format(self.screen_width, self.screen_height))
        self.root.title("Tetravex GUI application")
        self.root.config(bg="#707070")
        
        self.setup_menubar() 
        self.setup_canvas()
        
        # default game 3x3
        self.on_new_game(3)
        
    def open_about(self):
        popup = tk.Toplevel(self.root)
        popup.title("About")
        popup.geometry("400x300")

        msg = '\n'.join([
            "This is a Tetravex game clone",
            "Make all of the edges of the blocks match on the right",
            "Good luck!"
        ])

        label = tk.Label(popup, text=msg)
        label.pack(pady=20)
        
        close_button = tk.Button(popup, text="Okay", command=popup.destroy)
        close_button.pack()
        
        # center the popup
        popup.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry("+{}+{}".format(x, y))
    
    def open_prefs(self): 
        popup = tk.Toplevel(self.root)
        popup.title("Preferences Window")
        popup.geometry("400x400")

        label = tk.Label(popup, text="Color Theme:")
        label.pack(pady=5)

        # TODO change to radio button group instead ?
        valid_combobox_choices = ["Solarized", "High Contrast", "Randomized"]
        combo_var = tk.StringVar()
        combobox = ttk.Combobox(popup, textvariable=combo_var, values=valid_combobox_choices)
        combobox.pack(pady=5)
        combobox.set(valid_combobox_choices[0])
        self.color_map = self.colors.get_color(valid_combobox_choices[0])

        def on_combobox_select(event):
            selected_item = combo_var.get()
            # print("[INFO] Item =", selected_item)
            
            idx = valid_combobox_choices.index(selected_item)
            self.color_map = self.colors.get_color(idx)

            self.draw_canvas()
            return 
        
        combobox.bind("<<ComboboxSelected>>", on_combobox_select)

        # --- Checkbox widget ---- 
        checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(popup, text="Enable warning outline", variable=checkbox_var)
        
        def on_checkbox_change():
            self.show_wrong_tile = checkbox_var.get()
            self.draw_canvas()
            return

        checkbox.config(command=on_checkbox_change)
        checkbox.pack(pady=5)

        close_button = tk.Button(popup, text="Okay", command=popup.destroy)
        close_button.pack(pady=5)
        
        # center the popup
        popup.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry("+{}+{}".format(x, y))

    def setup_menubar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # --- File Menu ---
        file_menu = tk.Menu(menubar, tearoff=0)
        for i in range(2, 7):
            file_menu.add_command(label="{}x{}".format(i, i), command=lambda size=i: self.on_new_game(size) )

        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=lambda: self.on_quit() )
        menubar.add_cascade(label="File", menu=file_menu) 
        
        # --- Prefs Menu ---
        prefs_menu = tk.Menu(menubar, tearoff=0)
        prefs_menu.add_command(label="Open Prefs", command=self.open_prefs)
        menubar.add_cascade(label="Prefs", menu=prefs_menu)

        # --- About Menu ---
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Open About", command=self.open_about)
        menubar.add_cascade(label="About", menu=about_menu)

    def on_button1_event(self, event, *args, **kwargs):
        size = self.gm.engine.size
        tile = self.tile_size
        margin  = BOARD_MARGIN

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

        grid = self.gm.engine.grid
        if not grid:
            print("[E] No grid to draw")
            return

        numRows = len(grid)
        numCols = len(grid[0])

        if i < 0 or j < 0 or i >= numRows or j >= numCols:
            return

        if self.clicked_square:
            i1, j1 = self.clicked_square
            i2, j2 = i, j
            self.gm.make_move(i1, j1, i2, j2)
            self.clicked_square = None
        else:
            self.clicked_square = [i, j]  
        
        self.draw_canvas()
    
    def on_game_over(self):
        if self.seen_game_over:
            return 
        self.seen_game_over = 1 
        
        # --- Game over popup ---
        popup = tk.Toplevel(self.root)
        popup.title("Game over")
        popup.geometry("200x200")

        msg = '\n'.join([
            "You completed the puzzle!",
            "Congrats!"
        ])

        label = tk.Label(popup, text=msg)
        label.pack(pady=20)
        
        close_button = tk.Button(popup, text="Okay", command=popup.destroy)
        close_button.pack()
        
        # center the popup
        popup.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry("+{}+{}".format(x, y))

    def zoom_out(self):
        self.tile_size = max(MIN_TILE_SIZE, self.tile_size - 10)
        self.draw_canvas()

    def zoom_in(self):
        self.tile_size = min(MAX_TILE_SIZE, self.tile_size + 10)
        self.draw_canvas()

    def setup_canvas(self):
        self.tile_size = 100
        g = self.tile_size * 3 

        self.canvas = tk.Canvas(self.root, bg="#707070")
        self.canvas.pack(side='top', fill='both', expand=True)
        
        self.canvas.bind('<Button-1>', lambda event: self.on_button1_event(event) ) 
        self.root.bind('<Escape>', lambda event: self.on_quit() ) 
        
        self.root.bind('<Control-minus>', lambda event: self.zoom_out() )
        self.root.bind('<Control-equal>', lambda event: self.zoom_in() )
        self.canvas.focus_set()
    
    def draw_canvas(self):
        grid = self.gm.engine.grid 
        if not grid:
            print("[E] No grid to draw")
            return 

        numRows = len(grid)
        numCols = len(grid[0])
        self.canvas.delete('all')  # clear canvas
        wrong_coords = self.gm.get_wrong_coords()

        for i in range(numRows):
            for j in range(numCols):
                x0 = j * self.tile_size 
                y0 = i * self.tile_size 
                if j >= numCols // 2:  # add margin between boards
                    x0 += BOARD_MARGIN

                x1, y1 = x0 + self.tile_size, y0 + self.tile_size
                xc, yc = x0 + self.tile_size // 2, y0 + self.tile_size // 2

                reduced = False
                if self.clicked_square:
                    if (i == self.clicked_square[0] and j  == self.clicked_square[1]):
                        reduced = True 

                bg_color = self.colors.tan
                if reduced:
                    bg_color = self.colors.reduce_color(bg_color)

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_color)

                b = grid[i][j]
                if not b.enable:
                    continue

                # vertices for tile
                b_nw, b_ne, b_sw, b_se = (x0, y0), (x1, y0), (x0, y1), (x1, y1)
                b_c = (xc, yc)

                # text anchor positions
                tn = (x0 + int(self.tile_size * 0.50), y0 + int(self.tile_size * 0.25))
                te = (x0 + int(self.tile_size * 0.75), y0 + int(self.tile_size * 0.50))
                ts = (x0 + int(self.tile_size * 0.50), y0 + int(self.tile_size * 0.75))
                tw = (x0 + int(self.tile_size * 0.25), y0 + int(self.tile_size * 0.50))

                # Define edge data for looping
                edges = [b.n, b.e, b.s, b.w]
                triangles = [
                    [b_c, b_ne, b_nw],  # N
                    [b_c, b_se, b_ne],  # E
                    [b_c, b_sw, b_se],  # S
                    [b_c, b_nw, b_sw],  # W
                ]
                text_positions = [tn, te, ts, tw]

                # Draw each edge using a single loop
                for val, tri_pts, text_pos in zip(edges, triangles, text_positions):
                    color = self.color_map.get(val)
                    text_color = self.colors.get_font_color(color)
                    if reduced:
                        color = self.colors.reduce_color(color)

                    self.canvas.create_polygon(tri_pts, fill=color, width=2, outline='#000000')
                    self.canvas.create_text(
                        *text_pos, 
                        text=str(val), 
                        anchor=tk.CENTER, 
                        font=("Arial", int(self.tile_size * 0.15) ), 
                        fill=text_color
                    )

                # Draw wrong outline if needed
                if self.show_wrong_tile and [i, j] in wrong_coords:
                    self.canvas.create_rectangle(x0, y0, x1, y1, outline='#ff0000', fill='', width=4)
    
    def resize_window(self):
        grid = self.gm.engine.grid 
        if not grid:
            print("[E] No grid to draw")
            return 
        
        numRows = len(grid)
        numCols = len(grid[0])
        size = numRows 

        w = (self.tile_size * size * 2) + BOARD_MARGIN 
        h = (self.tile_size * size)
        self.root.geometry("{}x{}".format(w, h) )

    def on_new_game(self, size: int):
        # reset game vars
        self.clicked_square = None 
        self.seen_game_over = 0 

        # call game reset
        self.gm.new_game(size)
        self.resize_window()

    def on_quit(self):
        self.root.quit()
    
    def run(self):
        self.root.mainloop()

