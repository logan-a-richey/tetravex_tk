# main_canvas.py 

import tkinter as tk 

class MainCanvas:
    def __init__(self, root, controller):
        self.root = root 
        self.controller = controller
        
        self.canvas = tk.Canvas(self.root, bg="#707070")
        self.canvas.pack(side='top', fill='both', expand=True) 
        self.canvas.focus_set()

        # TODO put this in SettingsManager
        # self.tile_size = 100 
        # self.grid_margin = 50 

        # self.canvas = tk.Canavs(root, bg="#707070") 
        self.canvas.bind("<Button-1>", lambda event: self.on_click(event) )
        self.canvas.pack(side="top", fill="both", expand=True)
        
        self.root.bind('<Control-minus>', lambda event: self.on_zoom_out() )
        self.root.bind('<Control-equal>', lambda event: self.on_zoom_in() )


    def on_click(self, event):
        callback_on_click = self.controller.on_click
        callback_on_click(event.x, event.y)

    def redraw(self, board_state, settings_state):
        self.canvas.delete("all")
