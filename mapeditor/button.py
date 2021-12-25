import pygame
from pygame import Vector2, Surface, Rect


class Button:
    def __init__(self, *,
                label: str,
                position: Vector2,
                size: Vector2
                ):
        self.rect = Rect(
            position.x,
            position.y,
            size.x,
            size.y
        )
        self.label = label

    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, value):
        if value < 0:
            value = 0
        self.position = Vector2(value, self.y)

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, value):
        if value < 0:
            value = 0
        self.position = Vector2(self.x, value)

    def update(self, *args, **kwargs) -> None:
        pass

    def render(self, surf: Surface) -> None:
        pygame.draw.rect(surf, pygame.Color(0, 255, 0), self.rect, 1)