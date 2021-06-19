from pathlib import Path
from configparser import ConfigParser
from typing import Dict, List, TYPE_CHECKING

from kairo.engine.entity import Entity
from .tile import Tile

if TYPE_CHECKING:
    from pygame import Surface


class Map(Entity):
    def __init__(self, level_file: Path):
        super().__init__()
        # properties
        self.level_file = level_file
        self.map: List = []
        self.key: Dict[str, Dict] = {}

        self.load_level(self.level_file)

    def update(self) -> None:
        pass

    def render(self, surf: "Surface") -> None:
        pass
        # for i, tile in enumerate(self.map):
        #     tile.render()

    def is_free(self, x: int, y: int) -> bool:
        pass

    def get_tile(self, x: int, y: int) -> Tile:
        return Tile(self.map[y * self.width + x])

    def load_level(self, level_file: Path):
        self.key = {}
        parser = ConfigParser()
        parser.read(level_file)

        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")

        # Load Tiles
        for section in parser.sections():
            if len(section) == 1:
                description = dict(parser.items(section))
                self.key[section] = description

        self.width = len(self.map[0])
        self.height = len(self.map)
