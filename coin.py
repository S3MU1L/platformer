import pygame
class Coin:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load("coin.png"),(30,30))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

