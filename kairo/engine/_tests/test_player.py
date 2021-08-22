from pathlib import Path
from typing import List, Optional
from unittest.mock import patch

from pygame import Surface, Vector2

from kairo.engine.game import Game
from kairo.engine.player import Player
from kairo.map.tilemap import TILESIZE, LayerMap


def _setup_basic_player(with_map=False, sample_map_file: Optional[Path] = None) -> Player:
    Game.resources['girl-redhair-blueshirt-64px'] = Surface((64, 64))

    if with_map:
        assert sample_map_file is not None
        Game.resources['sample-tileset'] = Surface((256, 256))
        Game.new_entity(
            LayerMap(
                level_file=sample_map_file,
                resources=Game.resources,
            )
        )

    return Player(Vector2(2 * TILESIZE, 3 * TILESIZE))


def test_player_default_components() -> None:
    """
    Check that when the Player is created it has its necessary components
    available and correctly configured.
    """
    p1 = _setup_basic_player()

    assert p1.mover is not None
    assert p1.mover.speed == 4

    animator_component = p1.components.get('Animator')
    assert animator_component is not None
    assert animator_component.tileset == Game.resources['girl-redhair-blueshirt-64px']

    collider_component = p1.components.get('Collider')
    assert collider_component is not None
    assert collider_component.box.size > (0, 0)
    assert len(collider_component.layers) > 1


def test_player_movement() -> None:
    """
    Check if the Player moves in its update method according to its input
    """
    p1 = _setup_basic_player()

    expected_position = (64, 96)
    speed = p1.mover.speed
    assert p1.position == expected_position

    p1.update(keyboard_input=Vector2(0, 1))
    expected_position = (expected_position[0], expected_position[1] + speed)
    assert p1.position == expected_position

    p1.update(keyboard_input=Vector2(-1, -1))
    expected_position = (expected_position[0] - speed, expected_position[1] - speed)
    assert p1.position == expected_position

    # If there's no input, the position should not change
    p1.update()
    assert p1.position == expected_position


def test_player_mover_with_collider(sample_map_file: Path) -> None:
    """
    Test Player movement with map collision.
    The player should not move when it's trying to go to a blocked tile
    """
    from kairo.engine.components.animator import Animator

    p1 = _setup_basic_player(with_map=True, sample_map_file=sample_map_file)
    maps: List[LayerMap] = Game.get_all_by_type('LayerMap')
    p1.update_maps(maps)

    expected_position = (2 * TILESIZE, 3 * TILESIZE)
    speed = p1.mover.speed = TILESIZE
    assert p1.position == expected_position

    with patch.object(Animator, 'update', return_value=None):
        """
        sample map, with player initially at @:
            hhhhhh
            hwwwwh
            ha..dh
            ha@.dh
            hwwwwh
        """
        p1.update(keyboard_input=Vector2(1, 0))
        expected_position = (expected_position[0] + speed, expected_position[1])
        assert p1.position == expected_position

        p1.update(keyboard_input=Vector2(1, 0))
        assert p1.position == expected_position

        p1.update(keyboard_input=Vector2(0, 1))
        assert p1.position == expected_position

        p1.update(keyboard_input=Vector2(0, -1))
        expected_position = (expected_position[0], expected_position[1] - speed)
        assert p1.position == expected_position

        p1.update(keyboard_input=Vector2(-1, -1))
        assert p1.position == expected_position
