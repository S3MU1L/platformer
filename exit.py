import pygame

class Exit:
    def __init__(self,x,y):
        img = pygame.image.load("exit.png")
        self.image = pygame.transform.scale(img,(50,75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y