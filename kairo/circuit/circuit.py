from collections import deque
from pathlib import Path
from typing import Any, Dict, MutableSequence, Optional, Tuple

from pygame import Vector2
from pygame.surface import Surface

from kairo.circuit import OFF, ON
from kairo.circuit.connector import Connector
from kairo.circuit.power import Power
from kairo.engine.entity import Entity


class Circuit(Entity):
    def __init__(
        self, position: Optional[Vector2] = None
    ):  # level_file: Path, resources: Dict[str, Any]):
        super().__init__(position)

        # instance properties
        self.connectors: Dict[Tuple[int, int], Connector] = {}
        self.state = OFF
        self.stack: MutableSequence = deque()
        self.toggled_last_update = False

    def add_connector(self, connector: Connector) -> None:
        previous = self.connectors[(int(connector.position.x), int(connector.position.y))]

        self.connectors[(int(connector.position.x), int(connector.position.y))] = connector
        connector.setup_initial_connections()

    def get_connector(self, position: Vector2) -> Optional[Connector]:
        return self.connectors[(int(position.x), int(position.y))]

    def update(self, *args, **kwargs) -> None:
        '''
        Updates the state of the connectors starting from its Power sources.
        '''
        if not self.toggled_last_update:
            return
        self.toggled_last_update = False
        for conn in self.connectors.values():
            if isinstance(conn, Power):
                conn.update(self.state)

    def late_update(self):
        self.clear()

    def clear(self):
        for conn in self.connectors.values():
            conn.visited = False

    def turnon(self):
        self.state = ON
        self.clear()

    def turnoff(self):
        self.state = OFF
        self.clear()

    def toggle(self):
        self.toggled_last_update = True
        if self.state == ON:
            self.turnoff()
        else:
            self.turnon()

    def render(self, canvas: Surface) -> None:
        for conn in self.connectors.values():
            conn.render(canvas)
