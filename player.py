import pygame
pygame.mixer.init()
jump_fx = pygame.mixer.Sound("jump.wav")
jump_fx.set_volume(0.5)
WIDTH = 1000
from world import World
class Player:
    def __init__(self,x,y):
        img = pygame.transform.scale(pygame.image.load("guy1.png"),(40,80))
        img2 = pygame.transform.scale(pygame.image.load("guy2.png"),(40,80))
        img3 = pygame.transform.scale(pygame.image.load("guy3.png"),(40,80))
        img4 = pygame.transform.scale(pygame.image.load("guy4.png"),(40,80))

        self.right_pictures = [img,img2,img3,img4]

        img = pygame.transform.flip(img, 1, 0)
        img2 = pygame.transform.flip(img2, 1, 0)
        img3 = pygame.transform.flip(img3, 1, 0)
        img4 = pygame.transform.flip(img4, 1, 0)
        self.left_pictures  = [img,img2,img3,img4]
        self.dead = False
        self.image = pygame.transform.scale(img,(40,80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 5
        self.jumped = False
        self.orient = 1
        self.cooldown = 0
        self.moving = False
        self.vely = 0
        self.can = True

    def reset(self,x,y):
        self.dead = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 5
        self.jumped = False
        self.orient = 1
        self.cooldown = 0
        self.moving = False
        self.vely = 0
        self.can = True

    def draw(self,screen):
        index = 0
        if self.cooldown<=15:
            index = 0
        elif self.cooldown<=30:
            index = 1
        elif self.cooldown<=45:
            index = 2
        elif self.cooldown<=60:
            index = 3

        if self.dead == False:
            if self.orient==1:
                if self.moving == False:
                    screen.blit(self.right_pictures[0],self.rect)
                else:
                    screen.blit(self.right_pictures[index],self.rect)
            else:
                if self.moving == False:
                    screen.blit(self.left_pictures[0], self.rect)
                else:
                    screen.blit(self.left_pictures[index], self.rect)
            if self.cooldown >= 60:
                self.cooldown = 0
        if self.dead == True:
            screen.blit(self.image,self.rect)


    def move(self,tlist, platlist):
        self.moving = False
        dx = 0
        dy = 0
        if self.dead == True:
            self.rect.y -= 2

        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                dx = -5
                self.orient = 0
                self.moving = True
            if keys[pygame.K_RIGHT]:
                dx = 5
                self.orient = 1
                self.moving = True


            if keys[pygame.K_SPACE] and self.jumped == False:
                if self.can:
                    self.vely = -15
                    self.can = False
                    jump_fx.play()
                self.jumped = True


            if keys[pygame.K_SPACE] == False:
                self.jumped = False


            self.vely += 1
            if self.vely > 10:
                self.vely = 10
            dy+=self.vely

            if self.rect.bottom > 1000:
                self.rect.bottom = 1000

            self.cooldown += 1

            for tile in tlist:

                if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                    dx = 0

                if tile[1].colliderect(self.rect.x,self.rect.y+dy,self.image.get_width(),self.image.get_height()):
                    if self.vely < 0:
                        dy = tile[1].bottom-self.rect.top
                        self.vely += 1

                    else:
                        dy = tile[1].top-self.rect.bottom
                        self.can = True

            for p in platlist:
                if p.rect.colliderect(self.rect.x+dx, self.rect.y,self.image.get_width(),self.image.get_height()):
                    # in x direction
                    dx = 0
                if p.rect.colliderect(self.rect.x,self.rect.y+dy,self.image.get_width(),self.image.get_height()):
                    if abs(self.rect.top +dy-p.rect.bottom)<15:
                        self.vely = 0
                        dy = p.rect.bottom - self.rect.top

                    elif abs((self.rect.bottom + dy)-p.rect.top)<15:
                        self.rect.bottom = p.rect.top-1
                        dy = 0
                        self.can = True
                    if self.moving == False and p.direction==1:
                        self.rect.x += p.vel

            self.rect.x += dx
            self.rect.y += dy

        #check for collision with enemies
    def collision(self,elist,lavalist):
        for enemy in elist:
            if enemy.rect.colliderect(self.rect):
                x = self.rect.x
                y = self.rect.y
                self.image = pygame.transform.scale(pygame.image.load("ghost.png"),(50,80))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

                return True

        for lava in lavalist:
            if lava.rect.colliderect(self.rect):
                x = self.rect.x
                y = self.rect.y
                self.image = pygame.transform.scale(pygame.image.load("ghost.png"), (50, 80))
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

                return True

        return False

    def next_level(self,exit_list):
        for exit in exit_list:
            if exit.rect.colliderect(self.rect):
                return True
        return False