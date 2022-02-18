import pickle
import pygame
from world import World
from player import Player
import os


pygame.font.init()
pygame.init()
WIDTH = 1000
HEIGHT = 1000
timer = pygame.time.Clock()
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Budget Mario")
tile_size = 50
started = False
myfont = pygame.font.SysFont("comicsans",30)
level = 0


#loading images
bg = pygame.transform.scale(pygame.image.load("mountain.png"),(WIDTH,HEIGHT))
res_img = pygame.transform.scale(pygame.image.load("restart_btn.png"),(175,80))
start_img = pygame.image.load("start_btn.png")
exit_img = pygame.transform.scale(pygame.image.load("exit_btn.png"),(279,126))

#loading sounds
pygame.mixer.init()
coin_fx = pygame.mixer.Sound("coin.wav")
coin_fx.set_volume(0.5)
over_fx = pygame.mixer.Sound("game_over.wav")
over_fx.set_volume(0.5)

#load music
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1,0.0,5000)
def reset_level(level,player,world):
    player.reset(100,HEIGHT-130)
    world.exit_list.clear()
    world.lava_list.clear()
    world.enemies_list.clear()
    world.platform_list.clear()
    world.coin_list.clear()
    if os.path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    return world


class Button:
    def __init__(self,x,y,image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.clicked = False

    def check(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked==False:
                return True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return False

restart = Button(WIDTH//2-70,HEIGHT//2,res_img)
start = Button(121,HEIGHT//2,start_img)
exit = Button(600,HEIGHT//2,exit_img)

#load in level data and create world
if os.path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)



def draw_window(game_over,player,world,score):
    screen.blit(bg,(0,0))
    world.draw(screen)
    world.draw_enemies(screen)
    world.draw_lava(screen)
    world.draw_exit(screen)
    world.draw_platforms(screen)
    world.draw_coins(screen)
    text = myfont.render(f'SCORE: {score}',False,(0,255,0))
    screen.blit(text,(0,0))
    player.draw(screen)

    if game_over == True:
        screen.blit(restart.image,restart.rect)
    if restart.check()==True:
        main()
    pygame.display.update()

def draw_menu():
    global started
    string = "Jumping on top of enemies won't destroy them"
    text = myfont.render(string.upper(),False,(255,0,0))
    insp = myfont.render("Idea and pictures from : Coding with Russ",False,(255,0,0))
    screen.blit(bg,(0,0))
    screen.blit(text,(100,300))
    screen.blit(insp,(200,950))
    screen.blit(start.image,start.rect)
    screen.blit(exit.image,exit.rect)
    if exit.check()==True:
        pygame.quit()
    if start.check()==True:
        started = True
    pygame.display.update()


def main():
    run = True
    game_over = False
    global started
    global level
    global score
    score = 0
    level = 0
    player = Player(100, HEIGHT - 130)
    world = World(world_data)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if started == False:
            draw_menu()
        else:
            player.move(world.tile_list, world.platform_list)

            #checking if player collected a coin
            for coin in world.coin_list:
                if player.rect.colliderect(coin.rect) and player.dead==False:
                    world.coin_list.remove(coin)
                    score+=1
                    coin_fx.play()

            if player.collision(world.enemies_list,world.lava_list):
                game_over = True
                if player.dead==False:
                    over_fx.play()
                player.dead = True

            if player.next_level(world.exit_list):
                level+=1
                if level <= 7:
                    world = reset_level(level,player,world)
                else:
                    started = False
                    level = 0
            draw_window(game_over,player,world,score)
        timer.tick(FPS)

main()

