from typing import Optional

from pygame import Vector2

from kairo.circuit import OFF, ON
from kairo.circuit.connector import Connector
from kairo.engine.geometry import DIRECTION


class TransistorNPN(Connector):
    def __init__(self, state: int = 0, position: Optional[Vector2] = None, parent=None):
        super().__init__(state, position, parent)
        self.direction = DIRECTION['UP']
        self.control: Optional[Connector] = None
        self.is_active = False

    def _update(self, *args, **kwargs) -> bool:
        other: Optional[Connector] = kwargs.get('connector')

        if self.control is None:
            self.is_active = False

        if other is not None and other is self.control and not self.is_active:
            # # if it's switching the state, just cache it on previous_state for the next update
            # if self.previous_state == other.state:
            #     self.state = other.state
            # self.previous_state = other.state
            self.is_active = other.state == ON
            return True

        # if it is OFF, it will always transmit OFF independent of the input state
        state = kwargs.get('state') if self.is_active else OFF
        assert state is not None
        self.state = state
        for connection in self.connections:
            connection.update(state=state)

        return True

    def setup_initial_connections(self) -> None:
        '''
        Overridden so we can set the control input.
        '''
        control = self.circuit.get_connector(self.position + self.direction)
        if control:
            self.control = control
            control.connect(self)

        for direction in [self.direction.rotate(90), self.direction.rotate(-90)]:
            neighbour = self.circuit.get_connector(self.position + direction)
            if neighbour is not None:
                self.connect(neighbour)

    def connect(self, other: Connector) -> None:
        if other.position == self.position + self.direction:
            self.control = other
            return

        if other not in self.connections:
            self.connections.append(other)
            other.connect(self)
