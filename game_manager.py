# game_manager.py

from app import App
from engine import Engine 

class GameManager:
    def __init__(self):
        self.app = App()
        self.engine = Engine()

        self.app.gm = self
        self.engine.gm = self

        self.app.finish_init()

    def new_game(self, size: int):
        self.engine.new_game(size) 
        self.draw_canvas() 

    def draw_canvas(self):
        self.app.draw_canvas() 

    def run(self):
        self.app.run()

