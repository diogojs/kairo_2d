from pathlib import Path
from textwrap import dedent
from typing import Any, Callable

import pytest
from pygame import Vector2

from kairo.map.tile import Tile
from kairo.map.tilemap import Map


@pytest.fixture
def sample_map_file(datadir: Path) -> Path:
    """
    Writes a file with data for a sample map.
    Returns the path of the saved file.
    """
    level_file = datadir / 'sample.map'

    sample_map_content = dedent(
        """
        [level]
        tileset = sample-tileset
        map = hhhhh
              hwwwh
              ha.dh
              hwwwh

        [.]
        name = floor
        block: false
        tile = 6,0
        variants = 7,4

        [h]
        name = hole
        block: false
        tile = 1,1

        [w]
        name = north-wall
        block: true
        tile = 0,3
        variants = 3,0

        [a]
        name = west-wall
        block: true
        tile = 0,4
        variants = 1,3

        [d]
        name = east-wall
        block: true
        tile = 1,4
        variants = 1,3
        """
    )

    level_file.write_text(sample_map_content)
    return level_file


def test_load_level(sample_map_file: Path) -> None:
    """
    Test that loading a sample map file correctly sets a Map properties and tiles
    """

    resources = {'sample-tileset': 'fake loaded image'}

    m = Map(sample_map_file, resources)

    assert m.tileset == 'fake loaded image'
    assert m.width == 5
    assert m.height == 4

    # smoke test just to be sure the content of the map is OK
    assert len(m.map) == 4
    assert m.map[1] == "hwwwh"

    expected_tile = Tile(
        name='west-wall', block=True, tileset_position=Vector2(0, 4), variants=Vector2(1, 3)
    )
    assert m.tiles_registry[m.map[2][1]] == expected_tile
    assert m.get_tile(1, 2) == expected_tile


def test_render_tilemap(
    use_pygame: Callable, datadir: Path, sample_map_file: Path, image_regression: Any
) -> None:
    import pygame

    from kairo.resources import IMGS_DIR

    # from kairo._tests import pygame_debug

    window = use_pygame((256, 256))

    tileset = pygame.image.load(IMGS_DIR / 'tileset-zeldalike-32px.png').convert()

    resources = {'sample-tileset': tileset}

    m = Map(sample_map_file, resources)
    m.render(window)

    # pygame_debug()

    img_datapath = datadir / 'test_render_tilemap_image.png'
    pygame.image.save(window, img_datapath)

    image_regression.check(img_datapath.read_bytes())
