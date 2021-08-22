# Fixtures configuration for pytest

from pathlib import Path
from typing import Generator, Tuple

import pytest


@pytest.fixture
def use_pygame() -> Generator:
    """
    Returns a function that initialize pygame and setup the window with given window_size
    """

    import pygame
    from pygame.surface import Surface

    def set_pygame_window(window_size: Tuple[int, int] = (320, 160)) -> Surface:

        pygame.init()

        # Initialize game window
        window = pygame.display.set_mode((window_size[0], window_size[1]))
        pygame.display.set_caption("Kairo test")

        return window

    yield set_pygame_window

    pygame.quit()


@pytest.fixture
def sample_map_file(datadir: Path) -> Path:
    """
    Writes a file with data for a sample map.
    Returns the path of the saved file.
    """
    from textwrap import dedent

    level_file = datadir / 'sample.map'

    sample_map_content = dedent(
        """
        [level]
        tileset = sample-tileset

        [default]
        map = hhhhhh
              hwwwwh
              ha..dh
              ha..dh
              hwwwwh

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
