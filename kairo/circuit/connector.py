from pathlib import Path
from typing import Any, Dict, List, Optional

from pygame import Vector2

from kairo.circuit import OFF, ON
from kairo.engine.entity import Entity
from kairo.map.tilemap import LayerMap, Layers


class Connector(Entity):
    '''
    An abstract connector that can be specialized into circuit components (e.g. wire, transistor, etc)
    It defines the basic functionality of an eletronical connector.
    '''
    def __init__(self, state: int = 0, position: Optional[Vector2] = None, parent=None):
        super().__init__(position, parent)

        # instance properties
        self.circuit = self.parent
        self.state = state
        self.visited = False
        self.connections: List[Connector] = []

    def update(self, *args, **kwargs) -> None:
        if self.visited:
            return

        state = kwargs.get('state')

        self.visited = True
        self.circuit.stack.append(self)

        # Update state
        if state in [ON, OFF]:
            self.state = state
        else:
            self.state = OFF

        for connection in self.connections:
            connection.update(state=self.state)

        if len(self.parent.stack) > 0:
            self.parent.stack.pop()

    def load_circuit_from(self, level_file: Path, resources: Dict[str, Any]):
        self.map_representation = LayerMap(level_file, resources, Layers.CIRCUIT)
