from pathlib import Path
from textwrap import dedent
from typing import Any, Callable

import pytest
from pygame import Vector2

from kairo.circuit.circuit import Circuit
from kairo.circuit.power import Power
from kairo.circuit.wire import Wire
from kairo.engine.event_queue import EventQueue


@pytest.fixture
def event_queue() -> EventQueue:
    return EventQueue()


def _setup_circuit(event_queue: EventQueue) -> Circuit:
    '''
    ########
    ####|#-|
    #P--|###
    ####|-##
    ########
    '''
    circuit = Circuit(event_queue)
    connectors = []
    connectors.append(circuit.add_connector(Power(position=Vector2(1, 2), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(2, 2), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(3, 2), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(4, 1), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(4, 2), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(4, 3), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(5, 3), parent=circuit)))
    
    # Connectors id > 15 will be disconnected from the others
    connectors.append(circuit.add_connector(Wire(position=Vector2(6, 1), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(7, 1), parent=circuit)))

    return circuit


def test_circuit(event_queue: EventQueue) -> None:
    """
    Creates a circuit with some components and checks that everything is on its place.
    """
    circuit = _setup_circuit(event_queue)

    power = circuit.get_connector(Vector2(1, 2))
    assert power is not None
    assert not power.is_on()

    circuit.toggle()
    circuit.update()
    assert power.is_on()
    for connector in circuit.connectors.values():
        if connector.id > 15:
            assert not connector.is_on()
        else:
            assert connector.is_on()
    
    circuit.toggle()
    circuit.update()
    for connector in circuit.connectors.values():
        assert not connector.is_on()
