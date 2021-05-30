from typing import TYPE_CHECKING

from kairo.engine.entity import Entity

if TYPE_CHECKING:
    from pygame import Surface

s = ""
w = "w"

# fmt: off
LEVEL1 = [
    s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s,
    s, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, s,
    s, w, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, w, s,
    s, w, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, w, s,
    s, w, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, w, s,
    s, w, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, w, s,
    s, w, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, w, s,
    s, w, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, w, s,
    s, w, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, w, s,
    s, w, w, w, w, w, w, w, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, w, s,
    s, w, s, s, s, s, s, w, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, w, s,
    s, w, s, s, s, s, s, w, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, w, s,
    s, w, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, w, s,
    s, w, s, s, s, s, s, w, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, w, s,
    s, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, w, s,
    s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s,
]
# fmt: on


class Tile:
    def __init__(self, char: str):
        self.char = char


class Map(Entity):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.map = LEVEL1
        self.w = width
        self.h = height

    def update(self) -> None:
        pass

    def render(self, surf: Surface) -> None:
        pass
        # for i, tile in enumerate(self.map):
        #     tile.render()

    def is_free(self, x: int, y: int) -> bool:
        pass

    def get_tile(self, x: int, y: int) -> Tile:
        return Tile(self.map[y * self.w + x])
