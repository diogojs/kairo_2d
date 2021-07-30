from typing import Optional

from pygame import Rect, Surface, Vector2
from kairo.engine.components.mover import Mover
from kairo.engine.entity import Entity
from kairo.engine.game import Game


class Player(Entity):
    def __init__(self, position: Optional[Vector2] = None):
        super().__init__(position)

        self._current_map = Game.get_first_by_type('Map')
        self.tileset = Game.resources['tileset-zeldalike-32px']
    
        self.add_component(Mover())

    def update(self, *args, **kwargs) -> None:
        mover = self.components.get('Mover', Mover())
        mover.update(position=self.position, keyboard_input=kwargs.get('keyboard_input'), current_map=self._current_map)
        
    def render(self, surf: Surface):
        tilesize = 32
        rect = Rect(
            14*tilesize,
            5*tilesize,
            tilesize,
            tilesize,
        )
        surf.blit(self.tileset, (self.position.x * tilesize, self.position.y * tilesize), rect)
