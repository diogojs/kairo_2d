from pathlib import Path
from textwrap import dedent
from typing import Any, Callable

import pytest
from pygame import Vector2
from kairo.circuit.circuit import Circuit
from kairo.circuit.power import Power
from kairo.circuit.wire import Wire

from kairo.map.tile import Tile
from kairo.map.tilemap import LayerMap

@pytest.fixture
def event_queue() -> EventQueue:
    return EventQueue()



def _setup_circuit() -> Circuit:
    '''
    ########
    ####|###
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
    return circuit


def test_circuit() -> None:
    """
    Creates a circuit with some components and checks that everything is on its place.
    """
    event_queue = EventQueue()
    circuit = _setup_circuit()

    power = circuit.get_connector((1, 2))
    assert not power.is_on()

    circuit.toggle()
    circuit.update()
    assert not power.is_on()


def test_render_tilemap(
    use_pygame: Callable, datadir: Path, sample_map_file: Path, image_regression: Any
) -> None:
    import pygame

    from kairo.resources import IMGS_DIR

    # from kairo._tests import pygame_debug

    window = use_pygame((256, 256))

    tileset = pygame.image.load(IMGS_DIR / 'tileset-zeldalike-32px.png').convert()

    resources = {'sample-tileset': tileset}

    m = LayerMap(sample_map_file, resources)
    m.render(window)

    # pygame_debug()

    img_datapath = datadir / 'test_render_tilemap_image.png'
    pygame.image.save(window, img_datapath)

    image_regression.check(img_datapath.read_bytes())
