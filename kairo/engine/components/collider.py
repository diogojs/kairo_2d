from typing import List, Optional

from pygame import Rect, Surface, draw

from kairo.engine.entity import Entity
from kairo.engine.game import Game
from kairo.map.tilemap import Layers


class Collider(Entity):
    def __init__(
        self, box: Rect, parent: Optional[Entity] = None, layers: List[Layers] = [Layers.DEFAULT]
    ):
        super().__init__(parent=parent)

        self.box = box
        self.layers = layers

    @property
    def rect(self):
        if self.parent is None:
            return self.box

        return Rect(
            self.parent.position.x + self.box.left,
            self.parent.position.y + self.box.top,
            self.box.width,
            self.box.height,
        )

    def update(self, *args, **kwargs) -> None:
        """
        TODO: What does the collider do on Update?
        """
        pass

    def render(self, surf: Surface):
        import pygame

        if not Game.is_debugging:
            return

        draw.rect(surf, pygame.Color(0, 255, 0), self.rect, 1)
