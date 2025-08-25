# settings_manager.py 

import random 
from abc import ABC, abstractmethod 
from dataclasses import dataclass 
from typing import List

COLOR_TAN   = "#d2b48c"
COLOR_BLACK = "#000000"
COLOR_WHITE = "#d0d0d0"

@dataclass
class SettingsState:
    theme: "Theme"
    enable_bad_rect: bool 
    tile_size: int

class Theme:
    def __init__(self,
        name="SomeTheme",
        canvas_bg=COLOR_BLACK,
        grid_bg=COLOR_TAN,
        grid_outline=COLOR_BLACK,
        colors={},
        tri_outline=COLOR_BLACK,
    ):
        self.name = name
        
        self.canvas_bg = canvas_bg
        
        self.grid_bg = grid_bg
        self.grid_outline = grid_outline

        self.colors = colors
        self.tri_outline = tri_outline
    
class SettingsManager:
    def __init__(self):
        self.themes = []
        self.load_themes()
        
        self.current_theme: "Theme" = self.themes[0]
        self.enable_bad_rect: bool = True
        self.tile_size: int = 100

    def load_themes(self) -> None:
        # Theme 1
        solarized_colors = {
            0: "#0e0e0e", # black
            1: "#ed322f", # Red
            2: "#b58900", # Yellow
            3: "#859900", # Green
            4: "#bb3b06", # Orange
            5: "#2aa198", # Cyan
            6: "#207bd2", # Blue
            7: "#d33682", # Magenta
            8: "#6c71c4", # Violet
            9: "#808080", # Gray
        }
        solarized_theme = Theme(
            name="Solarized", 
            colors=solarized_colors
        )
        self.themes.append(solarized_theme)
        
        # Theme 2
        high_contrast_colors = {
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
        }
        high_contrast_theme = Theme(
            name="High Contrast",
            colors=high_contrast_colors
        )
        self.themes.append(high_contrast_theme)

        # Theme 3
        random_theme = self.generate_random_theme()
        self.themes.append(random_theme)

    def generate_random_theme(self) -> "Theme":
        random_colors = {}
        for i in range(10):
            rgb = [random.randint(50, 200) for _ in range(3)]
            random_colors[i] = "#{:02x}{:02x}{:02x}".format(*rgb)
        
        return Theme(
            name="Random", 
            colors=random_colors
        )
    
    def get_theme_names(self) -> List[str]:
        theme_names = []
        for theme in self.themes:
            theme_names.append(theme.name)
        return theme_names

    def set_theme(self, theme_name: str) -> None:
        for idx, theme in enumerate(self.themes):
            if theme.name == theme_name:
                if theme.name == "Random":
                    self.themes[idx] = self.generate_random_theme()
                    self.current_theme = self.themes[idx]
                    return
                self.current_theme = theme 
                return 
    
    def set_enable_bad_rect(self, var: bool) -> None:
        self.enable_bad_rect = var

    def set_tile_size(self, tile_size: int) -> None:
        self.tile_size = tile_size 

    def get_state(self) -> "SettingsState":
        return SettingsState(
            self.current_theme, 
            self.enable_bad_rect, 
            self.tile_size
        )

