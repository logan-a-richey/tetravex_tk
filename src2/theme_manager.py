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
    def __init__(self, name="", colors={}):
        self.name = name
        self.colors = colors

    def get_colors(self):
        return self.colors


class RandomTheme(Theme):
    def __init__(self, name="", colors={}):
        self.name = name
        self.colors = self.get_colors()

    def get_colors(self):
        colors = {}
        rgb = [random.randint(50, 200) for _ in range(3)]
        for i in range(10):
            colors[i] = "#{:02x}{:02x}{:02x}".format(*rgb)
        self.colors = colors
        return colors


class ThemeManager:
    def __init__(self):
        self.themes = {}
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
        })
        theme2 = CustomTheme(name="High Contrast", colors={
            0: '#202020', # dark gray
            1: '#ff0000', # red
            2: '#ffa500', # orange
            3: '#ffff00', # yellow
            4: '#00ff00', # green
            5: '#00ffff', # cyan
            6: '#0000ff', # blue
            7: '#ff00ff', # pink
            8: '#707070', # light gray
            9: '#e0e0e0', # white 

        })
        theme3 = RandomTheme()

        theme_lst = [theme1, theme2, theme3]
        for theme in theme_lst:
            self.themes[theme.name] = theme 
    
    def get_default_theme(self) -> "Theme":
        key = list(self.themes.keys())[0]
        return self.themes[key]


