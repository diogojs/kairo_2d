from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict, List

from pygame import Vector2
from pygame.surface import Surface

from kairo.engine.entity import Entity
from kairo.map.tile import Tile

TILESIZE = 32


class Map(Entity):
    def __init__(self, level_file: Path, resources: Dict[str, Any]):
        super().__init__()

        #  instance properties
        self.map: List = []
        self.tiles_registry: Dict[str, Tile] = {}
        self.width = 0
        self.height = 0

        self.load_level(level_file, resources)

    def update(self, *args, **kwargs) -> None:
        pass

    def render(self, canvas: Surface) -> None:
        map_surface = Surface((self.width * TILESIZE, self.height * TILESIZE))
        for y in range(self.height):
            for x in range(self.width):
                tile = self.get_tile(x, y)
                tile.render(map_surface, Vector2(x, y), self.tileset)

        canvas.blit(map_surface, (0, 0))

    def is_free(self, x: int, y: int) -> bool:
        tile = self.get_tile(x, y)
        return not tile.block

    def get_tile(self, x: int, y: int) -> Tile:
        """
        Returns what's at the specified position on the map.
        """
        return self.tiles_registry[(self.map[y][x])]

    def load_level(self, level_file: Path, resources: Dict[str, Any]):
        from kairo.engine.game import Game
        from kairo.map.tile import data_from_dict
        from kairo.resources import IMGS_DIR

        self.tiles_registry = {}
        self.map = []
        parser = ConfigParser()
        parser.read(level_file)

        tileset_name = parser.get("level", "tileset")
        self.tileset = resources[tileset_name]
        self.map = parser.get("level", "map").split("\n")

        # Load Tiles
        for section in parser.sections():
            if len(section) == 1:
                description = data_from_dict(dict(parser.items(section)))
                self.tiles_registry[section] = Tile(**description)

        self.width = len(self.map[0])
        self.height = len(self.map)
