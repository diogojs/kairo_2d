from pathlib import Path
from textwrap import dedent

from pygame import Vector2

from kairo.map.tile import Tile
from kairo.map.tilemap import Map


def test_load_level(datadir: Path) -> None:
    """
    Test that loading a sample map file correctly sets a Map properties and tiles
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
        tile = 0,6
        variants = 7,4

        [h]
        name = hole
        block: false
        tile = 1,1

        [w]
        name = north-wall
        block: true
        tile = 3,0
        variants = 3,0

        [a]
        name = west-wall
        block: true
        tile = 4,0
        variants = 1,3

        [d]
        name = east-wall
        block: true
        tile = 4,1
        variants = 1,3
        """
    )

    level_file.write_text(sample_map_content)
    resources = {'sample-tileset': 'fake loaded image'}

    m = Map(level_file, resources)

    assert m.tileset == 'fake loaded image'
    assert m.width == 5
    assert m.height == 4

    # smoke test just to be sure the content of the map is OK
    assert len(m.map) == 4
    assert m.map[1] == "hwwwh"

    expected_tile = Tile(
        name='west-wall', block=True, tileset_position=Vector2(4, 0), variants=Vector2(1, 3)
    )
    assert m.tiles_registry[m.map[2][1]] == expected_tile
    assert m.get_tile(1, 2) == expected_tile
