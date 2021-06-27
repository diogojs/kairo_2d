from pygame import Vector2

from kairo.map.tile import Tile
from kairo.map.tilemap import Map
from kairo.resources import IMGS_DIR, MAPS_DIR


def test_load_level() -> None:
    """
    Test that loading a sample map file correctly sets a Map properties and tiles
    """
    level_file = MAPS_DIR / "level01.map"

    m = Map(level_file)

    assert m.tileset == "tileset-zeldalike-32px.png"
    assert m.width == 32
    assert m.height == 16
    assert len(m.map) == 16

    # smoke test just to be sure the content of the map is OK
    assert m.map[1] == "hqwwwwwwwwwwwwwwwwwwwwwwwwwwwweh"

    expected_tile = Tile(
        name='west-wall', block=True, tileset_position=Vector2(4, 0), variants=Vector2(1, 3)
    )
    assert m.tiles_registry[m.map[2][1]] == expected_tile
    assert m.get_tile(1, 2) == expected_tile
