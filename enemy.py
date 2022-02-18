import pygame
tile_size = 50

class Enemy:
    def __init__(self,x,y):
        self.img = pygame.transform.scale(pygame.image.load("blob.png"),(tile_size,40))
        self.x = x
        self.y = y
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.direction = 1
        self.count = 0

    def update(self):
        self.x += self.direction
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.count += 1
        if abs(self.count) > 50:
            self.direction *= -1
            self.count *= -1
