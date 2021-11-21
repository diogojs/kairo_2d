from pathlib import Path
from typing import List, Optional

from pygame import Vector2
from pygame.surface import Surface

from kairo.circuit import OFF, ON
from kairo.engine.entity import Entity
from kairo.engine.geometry import DIRECTION


class Connector(Entity):
    '''
    An abstract connector that can be specialized into circuit components (e.g. wire, transistor, etc)
    It defines the basic functionality of an eletronical connector.
    '''

    def __init__(self, state: int = 0, position: Optional[Vector2] = None, parent=None):
        from kairo.engine.components.animator import Animator
        from kairo.engine.game import Game

        super().__init__(position, parent)

        # instance properties
        self.circuit = self.parent
        self.state = state
        self.visited = False
        self.connections: List[Connector] = []

        # graphical stuff
        tileset = Game.resources['girl-redhair-blueshirt-64px']
        self.animator = self.add_component(Animator(tileset=tileset, tilesize=64, parent=self))

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

    def connect(self, other: 'Connector') -> None:
        if other not in self.connections:
            self.connections.append(other)
            other.connect(self)

    def disconnect(self, other: 'Connector') -> None:
        if other in self.connections:
            self.connections.remove(other)
            other.disconnect(self)

    def setup_initial_connections(self) -> None:
        for direction in DIRECTION.values():
            neighbour = self.circuit.get_component(self.position + direction)
            if neighbour is not None:
                self.connect(neighbour)

    def remove(self):
        for connection in self.connections:
            connection.disconnect(self)

    def render(self, canvas: Surface) -> None:
        for component in self.components.values():
            component.render(canvas)

    def is_on(self) -> bool:
        return self.state > 0
