from configparser import ConfigParser
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List

from pygame import SRCALPHA, Vector2
from pygame.surface import Surface

from kairo.engine.entity import Entity
from kairo.map.tile import Tile

TILESIZE = 32


class Layers(Enum):
    BACKGROUND = auto()
    DEFAULT = auto()
    CIRCUIT = auto()
    PLAYER = auto()
    FOREGROUND = auto()


class LayerMap(Entity):
    def __init__(self, level_file: Path, resources: Dict[str, Any], layer: Layers = Layers.DEFAULT):
        super().__init__()

        #  instance properties
        self.map: List = []
        self.tiles_registry: Dict[str, Tile] = {}
        self.width = 0
        self.height = 0
        self.layer = layer

        self.load_level(level_file, resources)

    def update(self, *args, **kwargs) -> None:
        pass

    def render(self, canvas: Surface) -> None:
        map_surface = Surface((self.width * TILESIZE, self.height * TILESIZE), SRCALPHA)
        for y in range(self.height):
            for x in range(self.width):
                tile = self.get_tile(x, y)
                tile.render(map_surface, Vector2(x, y), self.tileset)

        canvas.blit(map_surface, (self.position.x * TILESIZE, self.position.y * TILESIZE))

    def is_free(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width) or not (0 <= y < self.height):
            return True

        tile = self.get_tile(x, y)
        return not tile.block

    def get_tile(self, x: int, y: int) -> Tile:
        """
        Returns what's at the specified position on the map.
        """
        return self.tiles_registry[(self.map[y][x])]

    def load_level(self, level_file: Path, resources: Dict[str, Any]):
        from kairo.map.loader import data_from_dict, position_from_string

        self.tiles_registry = {}
        self.map = []
        parser = ConfigParser()
        parser.read(level_file)

        tileset_name = parser.get("level", "tileset")
        self.tileset = resources[tileset_name]

        layer_name = self.layer.name.lower()
        self.map = parser.get(layer_name, "map").split("\n")

        if parser.has_option(layer_name, 'position'):
            self.position = position_from_string(parser.get(layer_name, 'position'))

        # Load Tiles
        for section in parser.sections():
            if len(section) == 1:
                description = data_from_dict(dict(parser.items(section)))
                self.tiles_registry[section] = Tile(**description)

        self.width = len(self.map[0])
        self.height = len(self.map)
