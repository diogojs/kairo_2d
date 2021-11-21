from typing import Optional

from pygame import Vector2

from kairo.circuit.connector import Connector


class Power(Connector):
    def __init__(self, state: int = 0, position: Optional[Vector2] = None):
        super().__init__(state, position)
