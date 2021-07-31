from typing import Optional, TYPE_CHECKING

from pygame import Surface, Vector2
from kairo.engine.entity import Entity
from kairo.map.tilemap import TILESIZE

if TYPE_CHECKING:
    from kairo.map.tilemap import Map

class Mover(Entity):
    def __init__(self, speed=5):
        super().__init__()

        self.speed = speed

    def update(self, *args, **kwargs) -> None:
        self.position = kwargs.get('position', Vector2(0, 0))
        self._current_map: Optional['Map'] = kwargs.get('current_map')

        kb_input = kwargs.get('keyboard_input', Vector2(0, 0))
        if self.try_move(kb_input):
            self.position += kb_input.elementwise() * self.speed
    
    def try_move(self, movement: Vector2) -> bool:
        try_x = int( (self.position.x + movement.x*self.speed)*TILESIZE )
        try_y = int( (self.position.y + movement.y*self.speed)*TILESIZE )

        if self._current_map is None:
            return False

        return self._current_map.is_free(try_x, try_y)        

    def render(self, surf: Surface):
        raise NotImplementedError
