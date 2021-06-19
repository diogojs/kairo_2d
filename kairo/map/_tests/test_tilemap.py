from kairo.map.tilemap import Map
from kairo.resources import MAPS_DIR, IMGS_DIR


def test_load_level() -> None:
    level_file = MAPS_DIR / "level01.map"

    m = Map(level_file)

    assert m.tileset == "tileset-zeldalike-32px.png"
    assert m.width == 32
    assert m.height == 16
    assert len(m.map) == 16

    # smoke test just to be sure the content of the map is OK
    assert m.map[1] == "hqwwwwwwwwwwwwwwwwwwwwwwwwwwwweh"
