# theme_manager.py

from abc import ABC, abstractmethod 
import random

class Theme(ABC):
    def __init__(self, name="", colors={}):
        self.name = name
        self.colors = colors

    @abstractmethod 
    def get_colors(self):
        raise NotImplementedError


class CustomTheme(Theme):
    def __init__(self, name="CustomTheme", colors={}):
        self.name = name
        self.colors = colors

    def get_colors(self):
        return self.colors


class RandomTheme(Theme):
    def __init__(self, name="Randomized", colors={}):
        self.name = name
        self.colors = self.get_colors()

    def get_colors(self):
        colors = {}
        
        for i in range(10):
            rgb = [random.randint(50, 200) for _ in range(3)]
            colors[i] = "#{:02x}{:02x}{:02x}".format(*rgb)
        
        colors["outline"] = "#000000"
        colors["grid_bg"] = "#D2B48C"
        
        self.colors = colors

        return colors


class ThemeManager:
    def __init__(self):
        self.themes = {}
        self.default_theme = None
        self.current_theme = None 
        
        self.load_themes()

    def load_themes(self):
        theme1 = CustomTheme(name="Solarized", colors={
            0: "#0e0e0e", # black
            1: "#ed322f",  # Red
            2: "#b58900",  # Yellow
            3: "#859900",  # Green
            4: "#cb4b16",  # Orange
            5: "#2aa198",  # Cyan
            6: "#207bd2",  # Blue
            7: "#d33682",  # Magenta
            8: "#6c71c4",  # Violet
            9: "#808080", # Gray
            "outline": "#000000", # black
            "grid_bg": "#D2B48C" # tan
        })
        theme2 = CustomTheme(name="High Contrast", colors={
            0: "#202020", # dark gray
            1: "#ff0000", # red
            2: "#ffa500", # orange
            3: "#ffff00", # yellow
            4: "#00ff00", # green
            5: "#00ffff", # cyan
            6: "#0000ff", # blue
            7: "#ff00ff", # pink
            8: "#707070", # light gray
            9: "#e0e0e0", # white 
            "outline": "#000000", # black
            "grid_bg": "#D2B48C" # tan

        })
        theme3 = CustomTheme(name="Stencil", colors={
            0: "#000000", 
            1: "#000000", 
            2: "#000000", 
            3: "#000000", 
            4: "#000000", 
            5: "#000000", 
            6: "#000000", 
            7: "#000000", 
            8: "#000000", 
            9: "#000000", 
            "outline" : "#ffffff",
            "grid_bg": "#707070"
        })

        theme4 = RandomTheme()

        theme_lst = [theme1, theme2, theme3, theme4]
        for theme in theme_lst:
            self.themes[theme.name] = theme 

        self.default_theme = theme1
        self.current_theme = self.default_theme 

    def get(self):
        return self.current_theme 

    def set(self, text):
        self.current_theme = self.themes.get(text, self.default_theme)

