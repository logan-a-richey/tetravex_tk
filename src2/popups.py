# popups.py

import tkinter as tk 

from abc import ABC, abstractmethod

class AbstractPopup(ABC):
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

    @abstractmethod
    def trigger(self):
        pass
    
    def center_popup(self, popup):
        popup.update_idletasks()
        
        # app dimensions
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()
        root_h = self.root.winfo_height()

        # popup dimensions
        popup_w = popup.winfo_width()
        popup_h = popup.winfo_height()
        
        # new popup position
        popup_x = root_x + (root_w // 2) - (popup_w // 2)
        popup_y = root_y + (root_h // 2) - (popup_h // 2)

        popup.geometry("+{}+{}".format(px, py) )


class PrefsPopup(AbstractPopup):
    def __init__(self, root, controller):
        super().__init__(root, controller)
        self.settings_manager = controller.settings_manager
        
        self.refresh = self.controller.refresh()

        current_settings = self.settings_manager.get_state() 

        self.radio_var_1 = tk.StringVar(current_settings.theme.name)
        self.checkbox_var_1 = self.BooleanVar(current_settings.enable_bad_rect)

    def on_radio_1(self):
        print("on_radio_1")
        var = self.radio_var_1.get()
        self.refresh()

    def on_checkbox_1(self):
        print("on_checkbox_1")
        var = self.checkbox_var_1.get()
        self.refresh()
        
    def trigger(self):
        popup = tk.Toplevel(self.root)
        popup.title("Preferences Window")
        popup.geometry("400x400")

        tk.Label(popup, text="Color Theme").pack(pady=4)
        
        theme_options = self.theme_manager.get_names()
        for option in theme_options:
            tk.Radiobutton(
                popup,
                text=option,
                variable=self.radio_var_1,
                value=option,
                command=self.on_radio_1
            ).pack(pady=4)

        self.center_popup()


class AboutPopup(AbstractPopup):
    def __init__(self, root, controller):
        super().__init__(root, controller)
    
    def trigger(self):
        popup = tk.Toplevel(self.root)
        popup.title("About Window")
        popup.geometry("500x400")

        label_1 = tk.Label(popup, text="How to play", bg='#777777', font=("Arial", 16))
        label_1.pack(pady=4)

        msg = '\n'.join([
            'This is a clone of the game Tetravex',
            'Click 2 coordinates to swap blocks.',
            'The goal is to move all of the blocks from the left grid to the right grid,',
            'such that all adjacent edges are matching in value.',
            'Try to do it in as few moves possible!'
        ])

        label_2 = tk.Label(popup, text=msg)
        label_2.pack(pady=4)

        label_3 = tk.Label(popup, text="Controls", bg='#777777', font=("Arial", 16))
        label_3.pack(pady=4)

        msg = '\n'.join([
            'CTRL N : New game',
            'CTRL H : Get hint',
            'CTRL - : Zoom out',
            'CTRL = : Zoom in',
            'ESCAPE : Quit program'
        ])
        label_4 = tk.Label(popup, text=msg, font="TkFixedFont", anchor="w", justify="left")
        label_4.pack(pady=4)

        close_button = tk.Button(popup, text="Okay", command=popup.destroy)
        close_button.pack(pady=20)

        self.center_popup()


class WinPopup(AbstractPopup):
    def __init__(self, root, controller):
        super().__init__(root, controller)
    
    def trigger(self):
        popup = tk.Toplevel(self.app.root)
        popup.title("Game over")
        popup.geometry("300x200")

        msg = '\n'.join([ "You completed the puzzle!", "Congrats!" ])
        label = tk.Label(popup, text=msg).pack(pady=20)
        
        close_button = tk.Button(popup, text="Okay", command=popup.destroy).pack(pady=4)
        
        self.center_popup()

