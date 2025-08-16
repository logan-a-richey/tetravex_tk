# app.py

import random
import tkinter as tk 

class Block:
    def __init__(self):
        # block coordinates
        self.i = i
        self.j = j 
        
        # edge values
        self.n = 0
        self.e = 0
        self.s = 0
        self.w = 0

class Logic:
    def __init__(self):
        pass 
    
    def new_game(self, size:int):
        self.grid = []

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.logic = Logic()

        self.screen_width, self.screen_height = (800, 600)
        self.root.geometry("{}x{}".format(self.screen_width, self.screen_height))
        self.root.title("Tetravex GUI application")
        self.root.config(bg="#707070")
        
        self.mouse_pos = (0, 0)

        self.setup_menubar() 
        self.setup_canvas()

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

    def on_mouse_motion(self, event, *args, **kwargs):
        ''' Method binded to canvas object '''
        self.mouse_pos = (event.x, event.y)
    
    def on_button1_event(self, event):
        print("Left click @ ({}, {})".format(event.x, event.y) )

    def setup_canvas(self):
        self.tile_size = 40
        g = self.tile_size * 3 

        self.canvas = tk.Canvas(self.root, bg="#707070")
        self.canvas.pack(side='top', fill='both', expand=True)
        
        self.canvas.bind('<Motion>', lambda event: self.on_mouse_motion(event) )
        self.canvas.bind('<Button-1>', lambda event: self.on_button1_event(event) ) 
        self.root.bind('<Escape>', lambda event: self.on_quit() ) 
        
        # self.root.bind('<Control-minus>', lambda event: self.zoom_out() )
        # self.root.bind('<Control-equal>', lambda event: self.zoom_in() )
        self.canvas.focus_set()

    def on_new_game(self, size: int):
        print("[INFO] New game, size={}".format(size))

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


if __name__ == "__main__":
    a = App()
    a.run()
