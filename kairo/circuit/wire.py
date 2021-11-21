from pathlib import Path
from typing import Any, Dict, List, Optional

from pygame import Vector2

from kairo.circuit.connector import Connector
from kairo.engine.entity import Entity
from kairo.map.tilemap import LayerMap, Layers


class Wire(Connector):
    def __init__(self, state: int = 0, position: Optional[Vector2] = None, parent=None):
        super().__init__(state, position, parent)
