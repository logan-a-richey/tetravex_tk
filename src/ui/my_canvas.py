# my_canvas.py

import tkinter as tk
from typing import Optional, Tuple, List, Callable

# TODO use inheritance
class MyCanvas:
    def __init__(self, 
        root, 
        handle_click: Callable[[int, int], None],
        theme_manager
    ):
        self.handle_click: Callable[[int, int], None] = handle_click
        self.theme_manager = theme_manager 

        self.tile_size: int = 100
        self.grid_margin: int = self.tile_size // 2
        
        self.canvas = tk.Canvas(root, bg="#707070")
        self.canvas.pack(side='top', fill='both', expand=True)
        
        self.canvas.bind('<Button-1>', lambda event: self.on_canvas_click(event) ) 
        self.canvas.focus_set()
    
    def on_canvas_click(self, event):
        self.handle_click(event.x, event.y)

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
    
    def refresh(self, 
        grid: List[List["Block"]],
        clicked_tile: Tuple[int, int],
        wrong_coords: List[Tuple[int, int]],
        hint_coords: List[Tuple[int, int]],
        enable_bad_rect: bool
    ):
        self.canvas.delete("all")

        current_theme = self.theme_manager.get()
        current_colors = current_theme.colors
        
        numRows = len(grid)
        numCols = len(grid[0])

        for i in range(numRows):
            for j in range(numCols):
                x0 = j * self.tile_size 
                y0 = i * self.tile_size 
                if j >= numCols // 2:
                    x0 += self.grid_margin
                x1 = x0 + self.tile_size
                y1 = y0 + self.tile_size
                
                # see if square has been clicked
                dimmed = False
                if clicked_tile:
                    if (i == clicked_tile[0] and j == clicked_tile[1]):
                        dimmed = True

                # draw grid
                bg_color = current_colors.get('grid_bg', '#000000')
                if dimmed:
                    bg_color = self.dim_color(bg_color)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_color)
                
                block = grid[i][j] 
                if block.active:
                    self.draw_block(block, x0, y0, x1, y1, current_colors, dimmed)
                
                # draw grid outline
                outline_color = current_colors.get('outline', '#000000')
                self.canvas.create_rectangle(x0, y0, x1, y1, fill='', outline=outline_color, width=2)

        # draw overlays
        for i in range(numRows):
            for j in range(numCols):
                x0 = j * self.tile_size 
                y0 = i * self.tile_size 
                if j >= numCols // 2:
                    x0 += self.grid_margin
                x1 = x0 + self.tile_size
                y1 = y0 + self.tile_size

                outline_color = "" 
                if (i, j) in wrong_coords:
                    outline_color = "#ff0000"
                if (i, j) in hint_coords:
                    outline_color = "#00ff00"
                
                if enable_bad_rect and outline_color:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='', outline=outline_color, width=4)
