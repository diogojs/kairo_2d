from pygame import Vector2
from typing import Any, Dict


def data_from_dict(description: Dict[str, str]) -> Dict[str, Any]:
    """
    Receives a dictionary that is only composed of strings and transforms it on its Tile-typed values.
    e.g. {'block': 'false'} -> {'block': False}
    """
    data = {
        'name': description.get('name', 'unnamed tile'),
        'block': bool_from_string(description.get('block', 'False')),
        'tileset_position': position_from_string(description.get('tile', '0,0')),
        'variants': position_from_string(description.get('variants', '1,1')),
        'animated': bool_from_string(description.get('animated', 'False')),
    }
    return data


def bool_from_string(string: str) -> bool:
    """
    Gets a string with value 'false' or 'true' and returns its corresponding bool value
    """
    from distutils.util import strtobool

    return bool(strtobool(string))


def position_from_string(string: str) -> Vector2:
    """
    Gets a string representing a tuple of two integers (e.g. '2, 3')
    and returns its Vector2 representation (e.g. Vector2(2, 3))
    """
    position = string.split(',')
    i, j = (int(p) for p in position)
    return Vector2(i, j)
