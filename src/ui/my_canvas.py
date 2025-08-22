# my_canvas.py

import tkinter as tk
from typing import Optional, Tuple, List, Callable

class MyCanvas:
    def __init__(self, app):
        self.app = app 
        self.root = app.root
        self.engine = app.engine 
        self.theme_manager = app.theme_manager

        self.tile_size: int = 100
        self.grid_margin: int = self.tile_size // 2
        
        self.clicked_tile: Optional[Tuple[int, int]] = None
        self.hint_tiles: List[Tuple[int, int]] = []
        self.bad_tiles: List[Tuple[int, int]] = [] 
        
        self.canvas = tk.Canvas(self.root, bg="#707070")
        self.canvas.pack(side='top', fill='both', expand=True)
        
        self.canvas.bind('<Button-1>', lambda event: self.on_canvas_click(event) ) 
        
        self.root.bind('<Escape>', lambda event: self.app.on_quit() ) 
        
        self.root.bind('<Control-minus>', lambda event: self.on_zoom_out() )
        self.root.bind('<Control-equal>', lambda event: self.on_zoom_in() )
        
        self.root.bind('<Control-n>', lambda event: self.app.on_new_game(self.app.last_size) )
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
    
    def on_make_move(self, i1, i2, j1, j2) -> None:
        self.engine.make_move(i1, i2, j1, j2)
        
        self.clicked_tile = None
        self.hint_tiles.clear() 
        self.bad_tiles = self.engine.get_wrong_coords() 

        self.on_canvas_draw() 
        
        res = self.engine.is_solved()
        if res:
            self.app.on_win_popup()
    
    def on_get_hint(self):
        if self.hint_tiles:
            i1 = self.hint_tiles[0][0] 
            j1 = self.hint_tiles[0][1]
            i2 = self.hint_tiles[1][0]
            j2 = self.hint_tiles[1][1] 
            self.on_make_move(i1, j1, i2, j2)
            
            self.hint_tiles.clear() 
        else:
            self.hint_tiles = self.engine.get_hint_coords() 
        self.on_canvas_draw()
    
    def on_canvas_click(self, event):
        coord = self.get_mouse_coordinates(event)
        if not coord:
            self.clicked_tile = None
            self.on_canvas_draw()
            return

        if self.clicked_tile:
            i1, j1, i2, j2 = coord[0], coord[1], self.clicked_tile[0], self.clicked_tile[1]
            self.on_make_move(i1, j1, i2, j2)
        else:
            self.clicked_tile = coord
            self.on_canvas_draw()

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
        
        # special highlight for stencil theme
        if (r == 0 and g == 0 and b == 0):
            return "#220022"

        offset = 40 
        r = max(0, r - offset)
        g = max(0, g - offset)
        b = max(0, b - offset)

        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def draw_block(self, block, x0, y0, x1, y1, current_colors: dict, dimmed: bool):
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
            tri_color = current_colors.get(val, '#000000')
            text_color = self.get_font_color(tri_color)
            if dimmed:
                tri_color = self.dim_color(tri_color)
            
            outline_color = current_colors.get('outline', '#000000')
            self.canvas.create_polygon(
                tri_pts, 
                fill=tri_color, 
                width=1, 
                outline=outline_color
            )
            
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
        current_colors = current_theme.colors

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
                bg_color = current_colors.get('grid_bg', '#000000')
                if dimmed:
                    bg_color = self.dim_color(bg_color)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_color)
                
                # draw block
                block = grid[i][j] 
                if block.active:
                    self.draw_block(block, x0, y0, x1, y1, current_colors, dimmed)
                
                # draw grid outline
                outline_color = current_colors.get('outline', '#000000')
                self.canvas.create_rectangle(x0, y0, x1, y1, fill='', outline=outline_color, width=2)

        # draw overlays
        for i in range(numRows):
            for j in range(numCols):
                x0 = j * tile 
                y0 = i * tile 
                if j >= numCols // 2:
                    x0 += self.grid_margin
                x1 = x0 + tile
                y1 = y0 + tile

                outline_color = "" 
                if (i, j) in self.bad_tiles:
                    outline_color = "#ff0000"
                if (i, j) in self.hint_tiles:
                    outline_color = "#00ff00"
                
                if self.app.enable_bad_rect and outline_color:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='', outline=outline_color, width=4)

    def on_zoom_in(self):
        MAX_SIZE = 200
        self.tile_size = min(MAX_SIZE, self.tile_size + 10)
        self.app.resize_window()
    
    def on_zoom_out(self):
        MIN_SIZE = 50
        self.tile_size = max(MIN_SIZE, self.tile_size - 10)
        self.app.resize_window()

