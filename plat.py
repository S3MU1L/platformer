import pygame

class Platform:
    def __init__(self,x,y,direction):
        self.direction = direction
        self.count = 0
        self.vel = 1
        self.x = x
        self.y = y
        #direction=0 means yplatform
        #direction = 1 means xplatform
        if self.direction==0:
            self.image = pygame.transform.scale(pygame.image.load("platform_y.png"),(50,20))

        else:
            self.image = pygame.transform.scale(pygame.image.load("platform_x.png"),(50,20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.direction==0:
            self.y += self.vel
        if self.direction==1:
            self.x += self.vel
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.count += 1
        if abs(self.count) > 50:
            self.count = -50
            self.vel *= -1