# main_canvas.py 

import tkinter as tk 

class MainCanvas(tk.Canvas):
    def __init__(self, root):
        self.tile_size = 100 
        self.grid_margin = 50 
        
        # self.canvas = tk.Canavs(root, bg="#707070") 
        self.pack(side="top", fill="both", expand=True)

        self.bind("<Button-1>", lambda event: self.on_click(event) )

    def on_click(self, event):
        self.controller(event.x, event.y)
