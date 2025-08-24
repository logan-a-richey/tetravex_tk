# controller.py 

from engine import Engine
from settings_manager import SettingsManager
from main_window import MainWindow

class Controller:
    def __init__(self, root):
        self.root = root 

        self.engine = Engine()
        self.settings_manager = SettingsManager()
        self.main_window = MainWindow(root, self)
        
        # setup new game
        self.on_new_game(3)

    def on_new_game(self, size: int):
        self.engine.new_game(size)
        self.refresh()
    
    def on_quit(self):
        self.root.quit()

    def on_click(self, x: int, y: int):
        print("on_click ({}, {})".format(x, y))

    def refresh(self):
        print("Controller::refresh() called")
        
        # board_state = self.engine.get_state()
        # settings_state = self.settings_manager.get_state() 
        # self.main_window.canvas.redraw(board_state, settings_state)


