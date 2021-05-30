import pygame
from pygame import Vector2, display, time

tile_size = 32
map_size = Vector2(32, 16)
fps = 60

running = False

def main():
    init()

    run()

    quit()

def init():
    # Initialize pygame, window, map and other essential objects
    pygame.init()

    # Load resources
    # ...

    # Initialize game window
    window_size = map_size.elementwise() * tile_size
    window = display.set_mode((int(window_size.x), int(window_size.y)))
    display.set_caption("Kairo")

    clock = time.Clock()

def run():
    running = True
    while running:
        processInput()
        update()
        render()
        clock.tick(fps)

def quit():
    pygame.quit()

def processInput():
    pass

def update():
    running = False

def render():
    pass