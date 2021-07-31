from typing import Dict, List, Optional

from pygame import Surface, Vector2

from kairo.engine.components.animator import Animator
from kairo.engine.components.mover import Mover
from kairo.engine.entity import Entity
from kairo.engine.game import Game
from kairo.map.tilemap import TILESIZE


class Player(Entity):
    def __init__(self, position: Optional[Vector2] = None):
        super().__init__(position)

        # References to other Entities
        self._current_map = Game.get_first_by_type('Map')

        # Components
        self.mover = Mover(speed=2)

        tileset = Game.resources['girl-redhair-blueshirt-64px']
        self.animator = Animator(tileset=tileset, tilesize=64, position_ref=self.position)

    def update(self, *args, **kwargs) -> None:
        kb_input = kwargs.get('keyboard_input')

        old_position = Vector2(self.position)
        # Component responsible for moving the Player
        self.mover.update(
            position=self.position, keyboard_input=kb_input, current_map=self._current_map
        )

        # Animating
        direction = self.position - old_position
        self.animator.update(direction=direction)

    def render(self, surf: Surface):
        self.animator.render(surf)

    def update_speed(self, increment: int) -> None:
        self.mover.speed += increment
