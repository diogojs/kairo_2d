from typing import TYPE_CHECKING, List

from pygame import Surface, Vector2

from kairo.engine.entity import Entity
from kairo.map.tilemap import TILESIZE

if TYPE_CHECKING:
    from kairo.map.tilemap import LayerMap


class Mover(Entity):
    def __init__(self, speed=5, parent=None, current_maps: List['LayerMap'] = []):
        super().__init__(parent=parent)

        self.speed = speed
        self.current_maps = current_maps

    def update(self, *args, **kwargs) -> None:
        if self.parent is None:
            return

        kb_input = kwargs.get('keyboard_input', Vector2(0, 0))

        if kb_input == Vector2(0, 0):
            return

        if self.try_move(kb_input):
            self.parent.position += kb_input.elementwise() * self.speed

    def try_move(self, movement: Vector2) -> bool:
        assert self.parent is not None

        collider = self.parent.components.get('Collider', None)
        if collider is None or len(self.current_maps) == 0:
            return True

        for point in ['topleft', 'topright', 'bottomleft', 'bottomright']:
            x = getattr(collider.rect, point)[0]
            y = getattr(collider.rect, point)[1]
            try_x = int((x + movement.x * self.speed) / TILESIZE)
            try_y = int((y + movement.y * self.speed) / TILESIZE)

            for m in self.current_maps:
                if m.layer not in collider.layers:
                    continue

                try_x -= int(m.position.x)
                try_y -= int(m.position.y)
                if not m.is_free(try_x, try_y):
                    return False

        return True

    def render(self, surf: Surface):
        raise NotImplementedError
