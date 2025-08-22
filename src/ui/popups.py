# popups 

import tkinter as tk
from abc import ABC, abstractmethod

class Popup(ABC):
    def __init__(self, app):
        self.app = app
    
    @abstractmethod
    def open_popup(self):
        raise NotImplementedError 

    def center_popup(self, popup) -> None:
        popup.update_idletasks()
        
        app_x0 = self.app.root.winfo_x()
        app_y0 = self.app.root.winfo_y()
        app_w = self.app.root.winfo_width()
        app_h = self.app.root.winfo_height()

        pop_w = popup.winfo_width()
        pop_h = popup.winfo_height()

        x = app_x0 + (app_w // 2) - (pop_w // 2)
        y = app_y0 + (app_h // 2) - (pop_h // 2)
        
        popup.geometry("+{}+{}".format(x, y))


class PrefsPopup(Popup):
    def __init__(self, app):
        super().__init__(app)

        current_theme = self.app.theme_manager.get()
        self.radio_var = tk.StringVar(value=current_theme.name)

        self.checkbox_var = tk.BooleanVar(value=self.app.enable_bad_rect) 

    def on_radio_change(self):
        text = self.radio_var.get()
        self.app.theme_manager.set(text)
        
        self.app.on_canvas_draw()
    
    def on_checkbox_change(self):
        val = self.checkbox_var.get()
        self.app.enable_bad_rect = val
        self.app.on_canvas_draw()

    def open_popup(self):
        popup = tk.Toplevel(self.app.root)
        popup.title("Preferences Window")
        popup.geometry("400x400")

        # --- Radio Label ---
        tk.Label(popup, text="Color Theme").pack(pady=4)
        
        # --- Radio Group ---
        valid_choices = list(self.app.theme_manager.themes.keys())

        self.current_theme = self.app.theme_manager.get()
        for choice in valid_choices:
            tk.Radiobutton( 
                popup,
                text=choice,
                variable=self.radio_var,
                value=choice,
                command=self.on_radio_change
            ).pack(pady=4)
        
        # --- Checkbox ---
        tk.Checkbutton(
            popup,
            text="Enable Bad Rect Outline",
            variable=self.checkbox_var,
            command=self.on_checkbox_change,
        ).pack(pady=20)

        # --- Close Button ---
        tk.Button(
            popup,
            text="Okay",
            command=popup.destroy,
        ).pack(pady=5)
        
        self.center_popup(popup)


class AboutPopup(Popup):
    def __init__(self, app):
        super().__init__(app)

    def open_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("About")
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
        
        self.center_popup(popup)


class WinPopup(Popup):
    def __init__(self, app):
        super().__init__(app)

    def open_popup(self):
        popup = tk.Toplevel(self.app.root)
        popup.title("Game over")
        popup.geometry("300x200")

        msg = '\n'.join([ "You completed the puzzle!", "Congrats!" ])
        label = tk.Label(popup, text=msg).pack(pady=20)
        
        close_button = tk.Button(popup, text="Okay", command=popup.destroy).pack(pady=4)
        
        self.center_popup(popup)

