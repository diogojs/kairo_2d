from typing import TYPE_CHECKING, Any, Dict, Optional

import pygame
from pygame import Vector2, display, time

from kairo.map.tilemap import TILESIZE, Map
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

    def __init__(self):

        pygame.init()

        # Initialize game window
        window_size = Game.map_size.elementwise() * TILESIZE
        self.window = display.set_mode((int(window_size.x), int(window_size.y)))
        display.set_caption("Kairo")

        # Load resources
        self.resources['tileset-zeldalike-32px'] = pygame.image.load(
            IMGS_DIR / 'tileset-zeldalike-32px.png'
        ).convert_alpha()

        self.clock = time.Clock()
        self.initialize()

    def initialize(self):
        """
        Initialize the Map, Player, and other essential objects.
        """
        Game.new_entity(Map(level_file=MAPS_DIR / "level01.map", resources=self.resources))
        # circuit = Game.new_object(Circuit.instance())
        # circuit.add_component(Game.new_object(Wire(Point(0, 5))))
        # circuit.add_component(Game.new_object(Wire(Point(1, 5))))

        # player = Game.new_object(Player(Point(4, 7)))
        # player.set_circuit(circuit)

    @classmethod
    def new_entity(cls, entity: "Entity") -> "Entity":
        cls.entities[entity.id] = entity
        return entity

    @classmethod
    def get_by_id(cls, id: int) -> Optional["Entity"]:
        return cls.entities.get(id)

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
        self.movement = Vector2(0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False
                    break
                elif event.key == pygame.K_LEFT:
                    self.movement.x = -1
                elif event.key == pygame.K_RIGHT:
                    self.movement.x = 1
                elif event.key == pygame.K_UP:
                    self.movement.y = -1
                elif event.key == pygame.K_DOWN:
                    self.movement.y = 1

    def update(self):
        pass

    def render(self):
        self.window.fill((0, 0, 0))
        for entity in self.entities.values():
            entity.render(self.window)
        display.flip()
