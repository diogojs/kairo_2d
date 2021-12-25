import pygame
from pygame import Vector2, display, freetype

from kairo.map.tilemap import TILESIZE
from .button import Button

class Editor:
    def __init__(self):
        self.create_window()
        self.running = False
        self.mousebuttondown = None
        self.clickable = []
        self.drawable = []
    
    def create_window(self):
        pygame.init()
        self.window = pygame.display.set_mode((1280, 800))
        pygame.display.set_caption("Map Editor")

    def run(self):
        self.running = True

        self.initialize()

        while self.running:
            self.processInput()
            self.update()
            self.render()
    
    def initialize(self):
        btn_size = Vector2(100, 80)
        import_button = Button(label="Import", position=Vector2(10, 10), size=btn_size)
        self.clickable.append(import_button)
        self.drawable.append(import_button)
    
    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False
                    break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mousebuttondown = event
    
    def update(self):
        for obj in self.clickable:
            obj.update(self.mousebuttondown)

    def render(self):
        self.window.fill((20, 20, 20))

        for obj in self.drawable:
            obj.render(self.window)

        display.flip()
    
    def quit(self):
        pygame.quit()