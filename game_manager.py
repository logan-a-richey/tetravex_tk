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

    def run(self):
        self.app.run()

