from typing import Optional

from pygame import Rect, Surface, Vector2

from kairo.engine.components.animator import Animator
from kairo.engine.components.collider import Collider
from kairo.engine.components.mover import Mover
from kairo.engine.entity import Entity
from kairo.engine.game import Game


class Player(Entity):
    def __init__(self, position: Optional[Vector2] = None):
        super().__init__(position)

        # References to other Entities
        self._current_map = Game.get_first_by_type('Map')
        tileset = Game.resources['girl-redhair-blueshirt-64px']

        # Components
        self.mover = Mover(speed=2, parent=self)

        self.animator = self.add_component(Animator(tileset=tileset, tilesize=64, parent=self))

        collider_box = Rect(
            22 - self.animator.sprite_anchor.x / 2, 36 - self.animator.sprite_anchor.y / 2, 22, 22
        )
        self.collider = self.add_component(Collider(box=collider_box, parent=self))

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
        if Game.is_debugging:
            text = f'{self.position} ({int(self.position.x / 32)}, {int(self.position.y / 32)})'
            text_pos = tuple(self.position.elementwise() + 32)  # type: ignore
            Game.debug_font.render_to(surf, dest=text_pos, text=text, fgcolor=(0, 255, 0))

        for component in self.components.values():
            component.render(surf)

    def update_speed(self, increment: int) -> None:
        self.mover.speed += increment
