from dataclasses import dataclass
from enum import IntEnum

from pygame import Rect, Vector2
from pygame.surface import Surface


class TileTypes(IntEnum):
    GROUND = 0
    BLOCK = 10
    INTERACTIVE = 20


@dataclass
class Tile:
    """
    Describe a tile from a tileset
    """

    name: str
    block: bool = False
    tileset_position: Vector2 = Vector2(0, 0)
    variants: Vector2 = Vector2(1, 1)
    animated: bool = False

    def render(self, canvas: Surface, position: Vector2, tileset: Surface) -> None:
        from kairo.map.tilemap import TILESIZE

        # if self.animated:
        #     x_displacement = randrange(int(self.variants.x))
        #     y_displacement = randrange(int(self.variants.y))
        #     tileset_position = self.tileset_position + Vector2(x_displacement, y_displacement)
        # else:
        #     tileset_position = self.tileset_position
        rect = Rect(
            self.tileset_position.x * TILESIZE,
            self.tileset_position.y * TILESIZE,
            TILESIZE,
            TILESIZE,
        )
        canvas.blit(tileset, (position.x * TILESIZE, position.y * TILESIZE), rect)
