import pytest
from pygame import Vector2

from kairo.circuit import ON
from kairo.circuit.circuit import Circuit
from kairo.circuit.power import Power
from kairo.circuit.transistor import TransistorNPN
from kairo.circuit.wire import Wire
from kairo.engine.event_queue import EventQueue


@pytest.fixture
def event_queue() -> EventQueue:
    return EventQueue()


def _setup_circuit(event_queue: EventQueue) -> Circuit:
    '''
    #############-|
    ####|##|--P####
    #P--|##|#######
    ####|--^--#####
    #########|#####
    '''
    circuit = Circuit()
    connectors = []
    connectors.append(circuit.add_connector(Power(position=Vector2(1, 2), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(2, 2), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(3, 2), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(4, 1), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(4, 2), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(4, 3), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(5, 3), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(6, 3), parent=circuit)))
    connectors.append(
        circuit.add_connector(TransistorNPN(position=Vector2(7, 3), parent=circuit))
    )  # id = 18
    connectors.append(circuit.add_connector(Wire(position=Vector2(8, 3), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(9, 3), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(9, 4), parent=circuit)))


    # Connectors 26 <= id <= 34 are connected to a separate power
    connectors.append(circuit.add_connector(Power(position=Vector2(10, 1), parent=circuit)))

    # Wires looping through the first power-circuit
    # connectors.append(circuit.add_connector(Wire(position=Vector2(5, 1), parent=circuit)))
    # connectors.append(circuit.add_connector(Wire(position=Vector2(6, 1), parent=circuit)))
    # Substitute by the looping circuit
    connectors.append(circuit.add_connector(Wire(position=Vector2(9, 1), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(8, 1), parent=circuit)))

    connectors.append(circuit.add_connector(Wire(position=Vector2(7, 1), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(7, 2), parent=circuit)))

    # Connectors id >= 36 will be disconnected from the others
    connectors.append(circuit.add_connector(Wire(position=Vector2(13, 0), parent=circuit)))
    connectors.append(circuit.add_connector(Wire(position=Vector2(14, 0), parent=circuit)))

    return circuit


def test_circuit(event_queue: EventQueue) -> None:
    """
    Creates a circuit with some components and checks that everything is on its place.
    """
    circuit = _setup_circuit(event_queue)

    power1 = circuit.get_connector(Vector2(1, 2))
    assert power1 is not None
    assert not power1.is_on()

    circuit.toggle()
    circuit.update()
    assert power1.is_on()
    for connector in circuit.connectors.values():
        if connector.id < 18:  # after that are off because of the transistor
            assert connector.is_on()
        elif connector.id < 26:
            assert not connector.is_on()
        else:
            break

    circuit.toggle()
    circuit.update()
    for connector in circuit.connectors.values():
        assert not connector.is_on()


def test_transistors(event_queue: EventQueue) -> None:
    """
    Check that the Transistors are working correctly
    """
    circuit = _setup_circuit(event_queue)
    original_update = Power.update

    def mocked_update(self, *args, **kwargs):
        '''
        Mock the Power.update method so we don't need to call the circuit.clear()
        to clear the visited state of all connectors.
        '''
        original_update(self, *args, **kwargs)

        # don't clear unless we are at the end of the timestep
        if len(self.parent.stack) > 0:
            return
        circuit.clear()

    Power.update = mocked_update  # type: ignore

    power1 = circuit.get_connector(Vector2(1, 2))
    assert power1 is not None
    assert not power1.is_on()
    power1.update(state=ON)

    assert power1.is_on()
    for connector in circuit.connectors.values():
        if connector.id < 18:  # after that are off because of the transistor
            assert connector.is_on()
        else:
            assert not connector.is_on()

    # transistor id = 18
    # Connectors 26 <= id <= 34 are connected to a separate power
    # Connectors id >= 36 will be disconnected from the others
    power2 = circuit.get_connector(Vector2(10, 1))
    assert power2 is not None
    power1.update(state=ON)
    power2.update(state=ON)
    for connector in circuit.connectors.values():
        if 26 <= connector.id <= 34:
            assert connector.is_on()
        else:
            continue

    power1.update(state=ON)
    assert power1.is_on()
    for connector in circuit.connectors.values():
        if connector.id <= 34:  # now everything in the connected circuit should be ON
            assert connector.is_on()
        else:
            break
