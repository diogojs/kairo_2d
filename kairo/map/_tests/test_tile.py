from pathlib import Path
from typing import Callable

import pytest
from pygame import Vector2

from kairo.map.tile import Tile, data_from_dict


def test_tile_default_values() -> None:
    expected_tile = Tile(name='unknown')
    assert expected_tile.name == 'unknown'
    assert expected_tile.block is False
    assert expected_tile.tileset_position == (0, 0)
    assert expected_tile.variants == (1, 1)

    with pytest.raises(TypeError, match=r'missing \d+ required positional argument'):
        Tile()  # type: ignore


def test_create_tile() -> None:
    expected_tile = Tile(
        name='other name', block=True, tileset_position=Vector2(3, 4), variants=Vector2(5, 6)
    )
    assert expected_tile.name == 'other name'
    assert expected_tile.block
    assert expected_tile.tileset_position == (3, 4)
    assert expected_tile.variants == (5, 6)


def test_data_from_dict() -> None:
    """
    Test that when receiving a dictionary that is only composed of strings
    data_from_dict() transforms it on its Tile-typed values.
    """
    raw_description = {
        'name': 'wall',
        'block': 'false',
        'tile': '4,0',
        'variants': '1,3',
    }

    expected_data = {
        'name': 'wall',
        'block': False,
        'tileset_position': Vector2(4, 0),
        'variants': Vector2(1, 3),
    }

    assert data_from_dict(raw_description) == expected_data


def test_render_tile(use_pygame: Callable, datadir: Path, image_regression) -> None:
    import pygame

    from kairo.map.tilemap import TILESIZE
    from kairo.resources import IMGS_DIR

    window = use_pygame((256, 256))

    tileset = pygame.image.load(IMGS_DIR / 'tileset-zeldalike-32px.png').convert()

    for i in range(3):
        for j in range(3):
            tile = Tile(name='wall', block=True, tileset_position=Vector2(i, j))
            tile.render(window, (TILESIZE * i * 2, TILESIZE * j * 2), tileset)

    img_datapath = datadir / 'test_render_tile_image.png'
    pygame.image.save(window, img_datapath)

    image_regression.check(img_datapath.read_bytes())
