# main_canvas.py 

import tkinter as tk 

# class MainCanvas(tk.Canvas):

class MainCanvas:
    def __init__(self, root, controller):
        self.root = root 
        self.controller = controller
        
        self.canvas = tk.Canvas(self.root, bg="#707070")
        self.canvas.pack(side='top', fill='both', expand=True) 
        
        self.canvas.bind("<Button-1>", lambda event: self.controller.on_click(event) )
        
        self.canvas.bind('<Control-minus>', lambda event: self.controller.on_zoom_out() )
        self.canvas.bind('<Control-equal>', lambda event: self.controller.on_zoom_in() )
        self.canvas.bind('<Control-n>', lambda event: self.controller.new_of_prev_size() )
        self.canvas.bind('<Control-h>', lambda event: self.controller.on_get_hint() )

        self.canvas.focus_set()

        self.canvas.pack(side="top", fill="both", expand=True)
    
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
    
    def draw_block(self, 
        block, 
        x0, y0, x1, y1, 
        tile_size,
        current_colors: dict, 
        dimmed: bool
    ):
        xc, yc = x0 + tile_size // 2, y0 + tile_size // 2
        b_c = (xc, yc)
        
        # vertices for tile
        b_nw, b_ne, b_sw, b_se = (x0, y0), (x1, y0), (x0, y1), (x1, y1)

        # text anchor positions
        tn = (x0 + int(tile_size * 0.50), y0 + int(tile_size * 0.25))
        te = (x0 + int(tile_size * 0.75), y0 + int(tile_size * 0.50))
        ts = (x0 + int(tile_size * 0.50), y0 + int(tile_size * 0.75))
        tw = (x0 + int(tile_size * 0.25), y0 + int(tile_size * 0.50))

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
                font=("Arial", int(tile_size * 0.15) ), 
                fill=text_color
            )
    
    def redraw(self, board_state, settings_state, square_state):
        self.canvas.delete("all")

        grid = board_state.grid
        numRows = board_state.num_rows
        numCols = board_state.num_cols

        tile = settings_state.tile_size
        grid_margin = tile // 2

        current_theme = settings_state.theme 
        current_colors = settings_state.theme.colors
        
        clicked_tile = square_state.clicked_square 

        for i in range(numRows):
            for j in range(numCols):
                x0 = j * tile 
                y0 = i * tile 
                if j >= numCols // 2:
                    x0 += grid_margin
                x1 = x0 + tile
                y1 = y0 + tile
                
                # see if square has been clicked
                dimmed = False
                if clicked_tile:
                    if (i == clicked_tile[0] and j == clicked_tile[1]):
                        dimmed = True

                # draw grid
                bg_color = current_theme.grid_bg
                if dimmed:
                    bg_color = self.dim_color(bg_color)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg_color)
                
                # draw block
                block = grid[i][j] 
                if block.active:
                    self.draw_block(block, x0, y0, x1, y1, tile, current_colors, dimmed)
                
                # draw grid outline
                outline_color = current_theme.grid_outline
                self.canvas.create_rectangle(x0, y0, x1, y1, fill='', outline=outline_color, width=2)

        # draw overlays
        for i in range(numRows):
            for j in range(numCols):
                x0 = j * tile 
                y0 = i * tile 
                if j >= numCols // 2:
                    x0 += grid_margin
                x1 = x0 + tile
                y1 = y0 + tile
            
                if settings_state.enable_bad_rect and (i, j) in square_state.bad_coords:
                    overlay_color = "#ff0000"
                    draw_overlay = True

                if (i, j) in square_state.hint_coords:
                    overlay_color = "#00ff00"
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='', outline=overlay_color, width=4)

