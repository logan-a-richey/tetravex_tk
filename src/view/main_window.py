# main_window.py

from abc import ABC, abstractmethod
import tkinter as tk 

from view.popups import PrefsPopup, AboutPopup, WinPopup
from view.main_canvas import MainCanvas 

class MainWindow(tk.Frame):
    def __init__(self, root, controller):
        self.root = root 
        self.controller = controller  

        self.prefs_popup = PrefsPopup(root, controller)
        self.about_popup = AboutPopup(root, controller)
        self.win_popup = WinPopup(root, controller)
        self.canvas = MainCanvas(root, controller)
        
        self.setup_menubar()

        root.bind("<Escape>", lambda event: root.quit() ) 

    def setup_menubar(self):
        # callback functions
        on_new_game     : callable = self.controller.on_new_game 
        on_quit         : callable = self.controller.on_quit 
        on_prefs_popup  : callable = self.prefs_popup.trigger
        on_about_popup  : callable = self.about_popup.trigger

        # menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # menu 1
        file_menu = tk.Menu(menubar, tearoff=0)
        for i in range(2, 9):
            my_label = "New {}x{}".format(i, i)
            file_menu.add_command(
                label=my_label,
                command=lambda size=i: on_new_game(size)
            )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: on_quit() )
        menubar.add_cascade(label="File", menu=file_menu)

        # menu 2
        prefs_menu = tk.Menu(menubar, tearoff=0)
        prefs_menu.add_command(label="Open Prefs", command=lambda: on_prefs_popup() )
        menubar.add_cascade(label="Preferences", menu=prefs_menu)

        # menu 3
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Open About", command=lambda: on_about_popup() )
        menubar.add_cascade(label="About", menu=about_menu)
        
        
