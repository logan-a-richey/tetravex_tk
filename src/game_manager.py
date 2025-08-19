# game_manager.py

from app import App
from engine import Engine 

from typing import List, Tuple

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
    
    def get_wrong_coords(self):
        return self.engine.get_wrong_coords()
    
    def get_hint(self) -> List[Tuple[int, int]]:
        hint_coords = self.engine.get_hint()
        return hint_coords

    def make_move(self, i1, j1, i2, j2):
        self.engine.make_move(i1, j1, i2, j2)
        self.draw_canvas() 
        
        res = self.engine.is_game_over()
        if res:
            self.app.on_game_over()

    def draw_canvas(self):
        self.app.draw_canvas() 

    def run(self):
        self.app.run()

