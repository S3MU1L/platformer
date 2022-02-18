import pygame
from enemy import Enemy
from lava import Lava
from exit import Exit
from plat import Platform
from coin import Coin
tile_size = 50

class World:
    def __init__(self,data):
        self.enemies_list = []
        self.tile_list = []
        self.lava_list = []
        self.exit_list = []
        self.platform_list = []
        self.coin_list = []
        #load images
        dirt = pygame.transform.scale(pygame.image.load("dirt.png"),(tile_size,tile_size))
        grass = pygame.transform.scale(pygame.image.load("grass.png"),(tile_size,tile_size))
        row_count = 0
        for row in data:
            col_count = 0
            for collumn in row:
                if collumn == 1:
                    img_rect = dirt.get_rect()
                    img_rect.x = tile_size*col_count
                    img_rect.y = tile_size*row_count
                    tile = (dirt,img_rect)
                    self.tile_list.append(tile)
                if collumn == 2:
                    img_rect = grass.get_rect()
                    img_rect.x = tile_size*col_count
                    img_rect.y = tile_size*row_count
                    tile = (grass,img_rect)
                    self.tile_list.append(tile)
                if collumn == 3:
                    x = tile_size * col_count
                    y = tile_size * row_count+10
                    enemy = Enemy(x, y)
                    self.enemies_list.append(enemy)
                if collumn == 4:
                    x = tile_size * col_count
                    y = tile_size * row_count
                    platform = Platform(x, y, 1)
                    self.platform_list.append(platform)
                if collumn == 5:
                    x = tile_size * col_count
                    y = tile_size * row_count
                    platform = Platform(x, y, 0)
                    self.platform_list.append(platform)
                if collumn == 6:
                    lava = Lava(col_count*tile_size,row_count*tile_size+tile_size//2)
                    self.lava_list.append(lava)
                if collumn == 7:
                    coin = Coin(col_count*tile_size+tile_size//2-15,row_count*tile_size)
                    self.coin_list.append(coin)
                if collumn == 8:
                    exit = Exit(col_count*tile_size,row_count*tile_size+tile_size//2)
                    self.exit_list.append(exit)

                col_count += 1
            row_count += 1

    def draw(self,screen):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])

    def draw_enemies(self,screen):
        for enemy in self.enemies_list:
            enemy.update()
            #print(enemy.rect.x)
            screen.blit(enemy.img,(enemy.rect.x,enemy.rect.y))


    def draw_lava(self,screen):
        for lava in self.lava_list:
            screen.blit(lava.img,(lava.x,lava.y))

    def draw_exit(self,screen):
        for exit in self.exit_list:
            screen.blit(exit.image,exit.rect)

    def draw_platforms(self,screen):
        for platform in self.platform_list:
            platform.update()
            screen.blit(platform.image,platform.rect)
    def draw_coins(self,screen):
        for coin in self.coin_list:
            screen.blit(coin.image,coin.rect)

