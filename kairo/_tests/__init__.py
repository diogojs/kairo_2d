"""
Helper functions to be used on tests

This module is supposed to be imported only on tests
"""


def pygame_debug() -> None:
    import pygame

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
