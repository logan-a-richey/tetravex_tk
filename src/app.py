# app.py 

import tkinter as tk 

# globals
MIN_TILE_SIZE = 30
MAX_TILE_SIZE = 150
BOARD_MARGIN = 20  # width of gap between boards

color_map = {
    0: '#202020', # dark gray
    1: '#ff0000', # red
    2: '#ffa500', # orange
    3: '#ffff00', # yellow
    4: '#00ff00', # green
    5: '#00ffff', # cyan
    6: '#0000ff', # blue
    7: '#ff00ff', # pink
    8: '#707070', # light gray
    9: '#e0e0e0', # white 
}

class App:
    def __init__(self):
        self.gm = None 

    def finish_init(self):
        self.root = tk.Tk()

        self.screen_width, self.screen_height = (800, 600)
        self.root.geometry("{}x{}".format(self.screen_width, self.screen_height))
        self.root.title("Tetravex GUI application")
        self.root.config(bg="#707070")
        
        self.mouse_pos = (0, 0)

        self.setup_menubar() 
        self.setup_canvas()
        
        # default game 3x3
        self.on_new_game(3)
        
        self.clicked_square = None 
        self.seen_game_over = 0 

    def setup_menubar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # --- File Menu ---
        file_menu = tk.Menu(menubar, tearoff=0)
        for i in range(3, 7):
            file_menu.add_command(label="{}x{}".format(i, i), command=lambda size=i: self.on_new_game(size) )

        file_menu.add_separator()

        file_menu.add_command(label="Quit", command=lambda: self.on_quit() )

        menubar.add_cascade(label="File", menu=file_menu) 

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
    
    def on_game_over(self):
        if self.seen_game_over:
            return 
        self.seen_game_over = 1 
        
        # --- Game over popup ---
        popup = tk.Toplevel(self.root)
        popup.title("Game over")
        popup.geometry("400x300")

        msg = '\n'.join([
            "You completed the puzzle!",
            "Congrats"
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
        # print("[INFO] Drawing canvas")
        
        grid = self.gm.engine.grid 
        if not grid:
            print("[E] No grid to draw")
            return 
        
        numRows = len(grid)
        numCols = len(grid[0])
        
        # clear canvas 
        self.canvas.delete('all')
        
        # draw in canvas
        wrong_coords = self.gm.get_wrong_coords()

        for i in range(numRows):
            for j in range(numCols):
                x0 = j * self.tile_size 
                y0 = i * self.tile_size 
                
                # NOTE add margin between left board and right board
                if (j >= numCols // 2):
                    x0 += BOARD_MARGIN

                x1 = x0 + self.tile_size 
                y1 = y0 + self.tile_size 
                xc = x0 + self.tile_size // 2
                yc = y0 + self.tile_size // 2

                self.canvas.create_rectangle(x0, y0, x1, y1, fill='#d2b48c')

                b = grid[i][j] 
                if not (b.enable):
                    continue
                
                b_nw = (x0, y0)
                b_ne = (x1, y0)
                b_sw = (x0, y1)
                b_se = (x1, y1)
                
                b_c  = (xc, yc)

                tn   = (x0 + int(self.tile_size * 0.50), y0 + int(self.tile_size * 0.25) )
                te   = (x0 + int(self.tile_size * 0.75), y0 + int(self.tile_size * 0.50) )
                ts   = (x0 + int(self.tile_size * 0.50), y0 + int(self.tile_size * 0.75) )
                tw   = (x0 + int(self.tile_size * 0.25), y0 + int(self.tile_size * 0.50) )
                
                # draw triangles
                # n edge
                text_color = "#000000" if b.n != 0 else "#ffffff"
                points = [b_c, b_ne, b_nw]
                self.canvas.create_polygon(points, fill=color_map.get(b.n), width=2, outline='#000000')
                self.canvas.create_text(*tn, text="{}".format(b.n), anchor=tk.CENTER, fill=text_color)

                # e edge
                text_color = "#000000" if b.e != 0 else "#ffffff"
                points = [b_c, b_se, b_ne]
                self.canvas.create_polygon(points, fill=color_map.get(b.e), width=2, outline='#000000' )
                self.canvas.create_text(*te, text="{}".format(b.e), anchor=tk.CENTER, fill=text_color)

                # s edge
                text_color = "#000000" if b.s != 0 else "#ffffff"
                points = [b_c, b_sw, b_se]
                self.canvas.create_polygon(points, fill=color_map.get(b.s), width=2, outline='#000000' )
                self.canvas.create_text(*ts, text="{}".format(b.s), anchor=tk.CENTER, fill=text_color)

                # w edge
                text_color = "#000000" if b.w != 0 else "#ffffff"
                points = [b_c, b_nw, b_sw]
                self.canvas.create_polygon(points, fill=color_map.get(b.w), width=2, outline='#000000' )
                self.canvas.create_text(*tw, text="{}".format(b.w), anchor=tk.CENTER, fill=text_color)

                if [i, j] in wrong_coords:
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
        print("[INFO] New game, size={}".format(size))
        self.gm.new_game(size)
        self.resize_window()
    
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

    def on_quit(self):
        self.root.quit()
    
    def run(self):
        self.root.mainloop()

