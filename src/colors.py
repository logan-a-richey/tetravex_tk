# colors.py 

import random 

class Colors:
    def __init__(self):
       self.tan = "#d2b48c"

    def get_color(self, mode: int) -> dict:
        if mode == 0:
            solarized_colors = {
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
            }
            return solarized_colors
        elif mode == 1:
            high_contrast_colors = {
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
            }
            return high_contrast_colors
        else:
            # random colors
            random_colors = {}
            for i in range(10):
                random_rgb = [random.randint(50,200) for _ in range(3)]
                hex_color = "#{:02x}{:02x}{:02x}".format(*random_rgb)
                random_colors[i] = hex_color
            return random_colors

    def reduce_color(self, color: str):
        # rgb = [max(0, int(color[i+1:i+3], 16) - 2) for i in range(3)]
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)

        offset = 40 
        r = max(0, r - offset)
        g = max(0, g - offset)
        b = max(0, b - offset)

        return "#{:02x}{:02x}{:02x}".format(r, g, b)
    def get_font_color(self, hex_color: str) -> str:
        '''
        Returns white or black based on perceptual brightness of the color.
        Input in format: #rrggbb
        '''
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        return "#ffffff" if luminance < 128 else "#000000"
