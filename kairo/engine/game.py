import random
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import pygame
from pygame import Vector2, display, freetype, time

from kairo.engine.inputs import KeyboardInput
from kairo.map.tilemap import TILESIZE, LayerMap, Layers
from kairo.resources import IMGS_DIR, MAPS_DIR

if TYPE_CHECKING:
    from kairo.engine.entity import Entity


class Game:
    """
    Main class for our game loop.
    """

    map_size = Vector2(32, 16)
    entities: Dict[int, "Entity"] = dict()
    resources: Dict[str, Any] = dict()
    controller_input = KeyboardInput()
    clock: time.Clock = time.Clock()

    # Debug
    is_debugging = True
    debug_font: freetype.Font  # type: ignore[name-defined]

    def __init__(self):

        pygame.init()
        self.__class__.debug_font = freetype.SysFont('Comic Sans MS', 14)
        random.seed()

        # Initialize game window
        window_size = Game.map_size.elementwise() * TILESIZE
        self.window = display.set_mode((int(window_size.x), int(window_size.y)))
        display.set_caption("Kairo")

        # Load resources
        self.resources['tileset-zeldalike-32px'] = pygame.image.load(
            IMGS_DIR / 'tileset-zeldalike-32px.png'
        ).convert_alpha()
        self.resources['tileset-zeldalike-32px-alpha'] = pygame.image.load(
            IMGS_DIR / 'tileset-zeldalike-32px-alpha.png'
        ).convert_alpha()
        self.resources['girl-redhair-blueshirt-64px'] = pygame.image.load(
            IMGS_DIR / 'ss-girl-redhair-blueshirt-64px.png'
        ).convert_alpha()

        self.initialize()

    def initialize(self):
        """
        Initialize the LayerMap, Player, and other essential objects.
        """
        from kairo.circuit.circuit import Circuit
        from kairo.circuit.power import Power
        from kairo.circuit.wire import Wire
        from kairo.engine.player import Player

        maps = [
            Game.new_entity(
                LayerMap(
                    level_file=MAPS_DIR / "level01.map",
                    resources=self.resources,
                    layer=Layers.BACKGROUND,
                )
            )
        ]
        maps.append(
            Game.new_entity(
                LayerMap(
                    level_file=MAPS_DIR / "level01.map",
                    resources=self.resources,
                    layer=Layers.DEFAULT,
                )
            )
        )
        circuit = Game.new_entity(Circuit())
        circuit.add_connector(Wire(False, Vector2(0, 5), circuit))
        circuit.add_connector(Wire(False, Vector2(1, 5), circuit))
        circuit.add_connector(Wire(False, Vector2(1, 6), circuit))
        circuit.add_connector(Wire(False, Vector2(1, 7), circuit))
        circuit.add_connector(Wire(False, Vector2(0, 7), circuit))
        circuit.add_connector(Power(False, Vector2(2, 6), circuit))

        self.player = Game.new_entity(Player(Vector2(4 * TILESIZE, 7 * TILESIZE)))
        # player.set_circuit(circuit)

        maps.append(
            Game.new_entity(
                LayerMap(
                    level_file=MAPS_DIR / "level01.map",
                    resources=self.resources,
                    layer=Layers.FOREGROUND,
                )
            )
        )

        # After adding all layers, we have to update player
        # It's better to do it here than to check it in every update iteration
        self.player.update_maps(maps)

    @classmethod
    def new_entity(cls, entity: 'Entity') -> 'Entity':
        cls.entities[entity.id] = entity
        return entity

    @classmethod
    def get_by_id(cls, id: int) -> Optional['Entity']:
        return cls.entities.get(id)

    @classmethod
    def get_first_by_type(cls, _class: str) -> Any:
        """
        Returns the first Entity that is an instance of _class.
        """
        for entity in cls.entities.values():
            if type(entity).__name__ == _class:
                return entity
        return None

    @classmethod
    def get_all_by_type(cls, _class: str) -> List[Any]:
        """
        Returns all Game Entities that are instances of _class.
        """
        return [entity for entity in cls.entities.values() if type(entity).__name__ == _class]

    def run(self):
        self.running = True
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)

    def quit(self):
        pygame.quit()

    def processInput(self):
        """
        Process keyboard inputs.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False
                    break
                elif event.key == pygame.K_KP_PLUS:
                    self.player.update_speed(1)
                elif event.key == pygame.K_KP_MINUS:
                    self.player.update_speed(-1)
                elif event.key == pygame.K_HOME:
                    self.__class__.is_debugging = not self.__class__.is_debugging

        self.movement = Vector2(0, 0)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.movement.x -= 1
        elif pressed_keys[pygame.K_RIGHT]:
            self.movement.x += 1
        if pressed_keys[pygame.K_UP]:
            self.movement.y -= 1
        elif pressed_keys[pygame.K_DOWN]:
            self.movement.y += 1

    def update(self, *args, **kwargs) -> None:
        for entity in self.entities.values():
            entity.update(keyboard_input=Vector2(self.movement))

    def render(self):
        self.window.fill((0, 0, 220))
        for entity in self.entities.values():
            entity.render(self.window)

        if self.__class__.is_debugging:
            text = f'FPS: {int(self.clock.get_fps())}'
            Game.debug_font.render_to(
                self.window,
                dest=(self.window.get_size()[0] - 60, 10),
                text=text,
                fgcolor=(0, 255, 0),
            )

        display.flip()
