from pathlib import Path
from typing import Any, Dict, List, Optional

from pygame import Vector2

from kairo.circuit.connector import Connector
from kairo.engine.entity import Entity
from kairo.map.tilemap import LayerMap, Layers


class Wire(Connector):
    def __init__(self, state: int = 0, position: Optional[Vector2] = None):
        super().__init__(state, position)

    def update(self, *args, **kwargs) -> None:
        pass

    def load_circuit_from(self, level_file: Path, resources: Dict[str, Any]):
        self.map_representation = LayerMap(level_file, resources, Layers.CIRCUIT)
