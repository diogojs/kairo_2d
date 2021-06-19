from typing import Any, List, TYPE_CHECKING, Dict, Optional

import pygame
from pygame import Vector2, display, time
from kairo.resources import MAPS_DIR

if TYPE_CHECKING:
    from kairo.engine.entity import Entity


class Game:
    """
    Main class for our game loop.
    """

    tile_size = 32
    map_size = Vector2(32, 16)
    entities: Dict[int, "Entity"] = dict()
    resources: Dict[str, Any] = dict()

    def __init__(self):

        pygame.init()

        # Load resources
        self.resources = {}
        # self.resources['tileset'] = pygame.image.load(TILESET_IMAGE).convert()

        # Initialize game window
        window_size = Game.map_size.elementwise() * Game.tile_size
        self.window = display.set_mode((int(window_size.x), int(window_size.y)))
        display.set_caption("Kairo")

        self.clock = time.Clock()
        self.initialize()

    def initialize(self):
        """
        Initialize the Map, Player, and other essential objects.
        """
        from kairo.map.tilemap import Map

        Game.new_entity(Map(level_file=MAPS_DIR / "level01.map"))
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
        pass
