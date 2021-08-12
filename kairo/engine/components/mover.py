from typing import TYPE_CHECKING, Optional

from pygame import Surface, Vector2

from kairo.engine.entity import Entity
from kairo.map.tilemap import TILESIZE

if TYPE_CHECKING:
    from kairo.map.tilemap import LayerMap


class Mover(Entity):
    def __init__(self, speed=5, parent=None):
        super().__init__(parent=parent)

        self.speed = speed

    def update(self, *args, **kwargs) -> None:
        if self.parent is None:
            return

        self._current_map: Optional['LayerMap'] = kwargs.get('current_map')

        kb_input = kwargs.get('keyboard_input', Vector2(0, 0))
        if self.try_move(kb_input):
            self.parent.position += kb_input.elementwise() * self.speed

    def try_move(self, movement: Vector2) -> bool:
        assert self.parent is not None

        collider = self.parent.components.get('Collider', None)
        if collider is None or self._current_map is None:
            return True

        for point in ['topleft', 'topright', 'bottomleft', 'bottomright']:
            x = getattr(collider.rect, point)[0]
            y = getattr(collider.rect, point)[1]
            try_x = int((x + movement.x * self.speed) / TILESIZE)
            try_y = int((y + movement.y * self.speed) / TILESIZE)
            if not self._current_map.is_free(try_x, try_y):
                return False

        return True

    def render(self, surf: Surface):
        raise NotImplementedError
