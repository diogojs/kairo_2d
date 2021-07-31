from typing import Dict, List, Optional

from pygame import Rect, Surface, Vector2
from kairo.engine.components.mover import Mover
from kairo.engine.entity import Entity
from kairo.engine.game import Game
from kairo.map.tilemap import TILESIZE


class Player(Entity):
    def __init__(self, position: Optional[Vector2] = None):
        super().__init__(position)

        # References to other Entities
        self._current_map = Game.get_first_by_type('Map')
        
        # Visuals
        self.tileset = Game.resources['girl-redhair-blueshirt-64px']
        self.tilesize = 64
        self.animations: Dict[str, Dict[str, List]] = {
            'idle': {
                'sprites': [(15,0), (15,1), (15,2), (15,1),],
                'fpc': [12],
            },
            'walk_up': {
                'sprites': [(8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8)],
                'fpc': [4],
            },
            'walk_down': {
                'sprites': [(10,0), (10,1), (10,2), (10,3), (10,4), (10,5), (10,6), (10,7), (10,8)],
                'fpc': [4],
            },
            'walk_left': {
                'sprites': [(9,0), (9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7), (9,8)],
                'fpc': [4],
            },
            'walk_right': {
                'sprites': [(11,0), (11,1), (11,2), (11,3), (11,4), (11,5), (11,6), (11,7), (11,8)],
                'fpc': [4],
            },
        }
        self.current_animation = self.animations['idle']
        self.current_sprite = 0
        self.sprite_frame_counter = 0
        self.sprite_anchor = Vector2(self.tilesize/2, self.tilesize)

        # Components
        self.add_component(Mover(speed=2))

    def update(self, *args, **kwargs) -> None:
        kb_input = kwargs.get('keyboard_input')

        old_position = Vector2(self.position)
        # Component responsible for moving the Player
        mover = self.components.get('Mover', Mover())
        mover.update(position=self.position, keyboard_input=kb_input, current_map=self._current_map)

        # Animating
        direction = self.position - old_position
        # Precedence order just for aesthetics
        if direction == Vector2(0,0):
            new_animation = self.animations['idle']
        if direction.y < 0:
            new_animation = self.animations['walk_up']
        elif direction.x > 0:
            new_animation = self.animations['walk_right']
        elif direction.x < 0:
            new_animation = self.animations['walk_left']
        elif direction.y > 0:
            new_animation = self.animations['walk_down']
        
        if self.current_animation != new_animation:
            self.current_animation = new_animation
            self.current_sprite = 0
        else:
            self.sprite_frame_counter += 1
            if self.sprite_frame_counter > self.current_animation['fpc'][0]:
                self.sprite_frame_counter = 0
                self.current_sprite = (self.current_sprite+1)%len(self.current_animation['sprites'])

    def render(self, surf: Surface):
        sprite = self.current_animation['sprites'][self.current_sprite]
        left_corner = self.position - self.sprite_anchor.elementwise()/2
        sprite_on_tileset = Rect(
            sprite[1]*self.tilesize,
            sprite[0]*self.tilesize,
            self.tilesize,
            self.tilesize,
        )
        surf.blit(self.tileset, (left_corner.x, left_corner.y), sprite_on_tileset)

    def update_speed(self, increment: int) -> None:
        mover = self.components.get('Mover', Mover())
        mover.speed += increment  # type: ignore[attr-defined]