from enum import IntEnum


class TileTypes(IntEnum):
    GROUND = 0
    BLOCK = 10
    INTERACTIVE = 20


class Tile:
    def __init__(self, char: str):
        self.char = char
