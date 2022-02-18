import pygame
tile_size = 50

class Lava:
    def __init__(self, x, y):
        self.img = pygame.transform.scale(pygame.image.load("lava.png"), (tile_size, tile_size//2))
        self.x = x
        self.y = y
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
