from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from pygame import Rect, Surface, Vector2

from kairo.engine.entity import Entity
from kairo.engine.game import Game
from kairo.map.tilemap import TILESIZE


@dataclass
class Animation:
    sprites: List[Tuple[int, int]]
    fps: int = 1

    @property
    def n_sprites(self) -> int:
        return len(self.sprites)


class Animator(Entity):

    IDLE = 'idle'
    WALK_UP = 'walk_up'
    WALK_DOWN = 'walk_down'
    WALK_LEFT = 'walk_left'
    WALK_RIGHT = 'walk_right'

    def __init__(self, tileset: Surface, tilesize: int, position_ref: Vector2):
        super().__init__(position_ref)

        self.tileset = tileset
        self.tilesize = tilesize
        self._animations: Dict[str, Animation] = {
            self.IDLE: Animation(
                sprites=[
                    (15, 0),
                    (15, 1),
                    (15, 2),
                    (15, 1),
                ],
                fps=5,
            ),
            self.WALK_UP: Animation(
                sprites=[(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)],
                fps=15,
            ),
            self.WALK_DOWN: Animation(
                sprites=[
                    (10, 0),
                    (10, 1),
                    (10, 2),
                    (10, 3),
                    (10, 4),
                    (10, 5),
                    (10, 6),
                    (10, 7),
                    (10, 8),
                ],
                fps=15,
            ),
            self.WALK_LEFT: Animation(
                sprites=[(9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8)],
                fps=15,
            ),
            self.WALK_RIGHT: Animation(
                sprites=[
                    (11, 0),
                    (11, 1),
                    (11, 2),
                    (11, 3),
                    (11, 4),
                    (11, 5),
                    (11, 6),
                    (11, 7),
                    (11, 8),
                ],
                fps=15,
            ),
        }

        self.current_animation = self._animations[self.IDLE]
        self.current_sprite = 0
        self.fps_counter = 0.0
        self.sprite_anchor = Vector2(self.tilesize / 2, self.tilesize)

    def update(self, *args, **kwargs) -> None:
        """
        Should receive as keyword argument a Vector2 indicating the direction to which the entity is moving
        """
        direction = kwargs.get('direction', Vector2(0, 0))

        # Precedence order just for aesthetics
        if direction == Vector2(0, 0):
            new_animation = self._animations[Animator.IDLE]
        if direction.y < 0:
            new_animation = self._animations[Animator.WALK_UP]
        elif direction.x > 0:
            new_animation = self._animations[Animator.WALK_RIGHT]
        elif direction.x < 0:
            new_animation = self._animations[Animator.WALK_LEFT]
        elif direction.y > 0:
            new_animation = self._animations[Animator.WALK_DOWN]

        if self.current_animation != new_animation:
            self.current_animation = new_animation
            self.current_sprite = 0
        else:
            self.fps_counter += Game.clock.get_time()  # type: ignore[union-attr]
            if self.fps_counter >= 1000.0 / self.current_animation.fps:
                self.fps_counter = 0.0
                self.current_sprite = (self.current_sprite + 1) % self.current_animation.n_sprites

    def render(self, surf: Surface):
        sprite = self.current_animation.sprites[self.current_sprite]
        left_corner = self.position - self.sprite_anchor.elementwise() / 2
        sprite_on_tileset = Rect(
            sprite[1] * self.tilesize,
            sprite[0] * self.tilesize,
            self.tilesize,
            self.tilesize,
        )
        surf.blit(self.tileset, (left_corner.x, left_corner.y), sprite_on_tileset)

    def __getitem__(self, key: str) -> Optional[Animation]:
        return self._animations[key]

    def __setitem__(self, key: str, value: Animation) -> Animation:
        self._animations[key] = value
        return value
