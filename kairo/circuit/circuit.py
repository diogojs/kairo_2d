from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict

from pygame.surface import Surface

from kairo.engine.entity import Entity
from kairo.map.tilemap import Layers


class Circuit(Entity):
    def __init__(self, level_file: Path, resources: Dict[str, Any]):
        super().__init__()

        # instance properties
        self.load_circuit_from(level_file, resources)

    def update(self, *args, **kwargs) -> None:
        pass

    def render(self, canvas: Surface) -> None:
        pass

    def load_circuit_from(self, level_file: Path, resources: Dict[str, Any]):
        self.map_representation = InteractiveMap(level_file, resources, Layers.CIRCUIT)
