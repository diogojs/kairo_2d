from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Dict, Tuple

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

    def render(self, canvas: Surface, position: Tuple, tileset: Surface) -> None:
        from kairo.map.tilemap import TILESIZE

        rect = Rect(
            self.tileset_position.x * TILESIZE,
            self.tileset_position.y * TILESIZE,
            TILESIZE,
            TILESIZE,
        )
        canvas.blit(tileset, position, rect)


def data_from_dict(description: Dict[str, str]) -> Dict[str, Any]:
    """
    Receives a dictionary that is only composed of strings and transforms it on its Tile-typed values.
    e.g. {'block': 'false'} -> {'block': False}
    """
    data = {
        'name': description.get('name', 'unnamed tile'),
        'block': bool_from_string(description.get('block', 'False')),
        'tileset_position': position_from_string(description.get('tile', '0,0')),
        'variants': position_from_string(description.get('variants', '1,1')),
    }
    return data


def bool_from_string(string: str) -> bool:
    """
    Gets a string with value 'false' or 'true' and returns its corresponding bool value
    """
    from distutils.util import strtobool

    return bool(strtobool(string))


def position_from_string(string: str) -> Vector2:
    """
    Gets a string representing a tuple of two integers (e.g. '2, 3')
    and returns its Vector2 representation (e.g. Vector2(2, 3))
    """
    position = string.split(',')
    i, j = (int(p) for p in position)
    return Vector2(i, j)
