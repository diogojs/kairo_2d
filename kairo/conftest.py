# Fixtures configuration for pytest

from typing import Callable, Generator, Tuple

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
