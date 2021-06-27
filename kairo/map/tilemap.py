from configparser import ConfigParser
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional

from pygame import image
from pygame.surface import Surface

from kairo.engine.entity import Entity
from kairo.map.tile import Tile

TILESIZE = 32


class Map(Entity):
    def __init__(self, level_file: Path):
        super().__init__()
        # properties
        # self.level_filename = level_file # maybe I don't need to save the level_filename
        self.map: List = []
        self.tiles_registry: Dict[str, Tile] = {}
        self.width = 0
        self.height = 0

        self.load_level(level_file)

    def update(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        map_surface = Surface((self.width * TILESIZE, self.height * TILESIZE))
        for y in range(self.height):
            for x in range(self.width):
                tile = self.get_tile(x, y)
                tile.render(map_surface, (x, y), self.tileset)

        surface.blit(map_surface, (0, 0))

    def is_free(self, x: int, y: int) -> bool:
        pass

    def get_tile(self, x: int, y: int) -> Tile:
        """
        Returns what's at the specified position on the map.
        """
        return self.tiles_registry[(self.map[y][x])]

    def load_level(self, level_file: Path):
        from kairo.map.tile import data_from_dict
        from kairo.resources import IMGS_DIR

        self.tiles_registry = {}
        self.map = []
        parser = ConfigParser()
        parser.read(level_file)

        tileset_name = parser.get("level", "tileset")
        self.tileset = image.load(IMGS_DIR / tileset_name).convert()
        self.map = parser.get("level", "map").split("\n")

        # Load Tiles
        for section in parser.sections():
            if len(section) == 1:
                description = data_from_dict(dict(parser.items(section)))
                self.tiles_registry[section] = Tile(**description)

        self.width = len(self.map[0])
        self.height = len(self.map)
