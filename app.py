# app.py 

import tkinter as tk 

color_map = {
    0: '#000000', # black
    1: '#ff0000', # red
    2: '#ffa500', # orange
    3: '#ffff00', # yellow
    4: '#00ff00', # green
    5: '#00ffff', # cyan
    6: '#0000ff', # blue
    7: '#ff00ff', # pink
    8: '#707070', # gray
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
        print("Left click @ ({}, {})".format(event.x, event.y) )

    def setup_canvas(self):
        self.tile_size = 80
        g = self.tile_size * 3 

        self.canvas = tk.Canvas(self.root, bg="#707070")
        self.canvas.pack(side='top', fill='both', expand=True)
        
        self.canvas.bind('<Button-1>', lambda event: self.on_button1_event(event) ) 
        self.root.bind('<Escape>', lambda event: self.on_quit() ) 
        
        # self.root.bind('<Control-minus>', lambda event: self.zoom_out() )
        # self.root.bind('<Control-equal>', lambda event: self.zoom_in() )
        self.canvas.focus_set()
    
    def draw_canvas(self):
        print("[INFO] Drawing canvas")

        self.canvas.delete('all')
        
        # draw grid :
        grid = self.gm.engine.grid 
        if not grid:
            print("[E] No grid to draw")
            return 
        
        numRows = len(grid)
        numCols = len(grid[0])
        
        for i in range(numRows):
            for j in range(numCols):
                x0 = j * self.tile_size 
                y0 = i * self.tile_size 
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
                
                # draw triangles
                # n edge

                points = [b_c, b_ne, b_nw]
                self.canvas.create_polygon(points, fill=color_map.get(b.n) )
                
                # e edge
                points = [b_c, b_se, b_ne]
                self.canvas.create_polygon(points, fill=color_map.get(b.e) )

                # s edge
                points = [b_c, b_sw, b_se]
                self.canvas.create_polygon(points, fill=color_map.get(b.s) )

                # w edge
                points = [b_c, b_nw, b_sw]
                self.canvas.create_polygon(points, fill=color_map.get(b.w) )
                
                # text
                # canvas.create_text(50, 120, text="Left Aligned\nText with Anchor", anchor=tk.NW, font=("Verdana", 14), fill="green")

    def on_new_game(self, size: int):
        print("[INFO] New game, size={}".format(size))
        self.gm.new_game(size)

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
