import pygame
import classes.player as PLAYER
import classes.platform as LEVEL
import classes.enemy as ENEMY
import os
import sys
import random


#pygame setup
pygame.init()
screen = pygame.display.set_mode((480, 800))
clock = pygame.time.Clock()
running = True
player = PLAYER.Player()
player.rect.x = 0
player.rect.y = 700
player_group = pygame.sprite.Group()
ground_list = pygame.sprite.Group()
plat_list = pygame.sprite.Group()
enem_list = pygame.sprite.Group()
bull_list = pygame.sprite.Group()
player_group.add(player)
max_height = 0 #score
steps = 10
ploc = []
eloc = []
tx   = 32
ty   = 32
i=0
max_platforms = max_enemies = 4
ground_dir = os.path.join(sys.path[0], "assets", "sprites", "Treasure Hunters", "Treasure Hunters", "Palm Tree Island", "Sprites", "Terrain", "Terrain (32x32).png")
while i <= (480/tx)+tx:
    ground_list.add(LEVEL.Platform(i*tx, 800-ty, ground_dir))
    i=i+1

while running:
    #event handler
    for event in pygame.event.get():
        #player clicks the X button
        if event.type == pygame.QUIT:
            running = False
    
    #generarte platforms
    if len(ploc) < max_platforms:
        ploc.append((random.randint(0,480-tx), 800-196*(len(ploc)+1), random.randint(1,9)))
        plat_list = LEVEL.platform(ploc, plat_list, 1)
    #generate cannons
    if len(eloc) < len(ploc):
        eloc.append((random.choice([0,480-30]), 800-196*(len(ploc))-32))
        enem_list = ENEMY.enemy(eloc, enem_list, 1)

    screen.fill((0, 0, 0))
    ground_list.draw(screen)
    plat_list.draw(screen)
    enem_list.draw(screen)
    bull_list.draw(screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.rect.x > 0:
        player.move(-steps)
    if keys[pygame.K_d] and player.rect.x < 420:
        player.move(steps)
        
    #shoot bullets
    if len(bull_list) < 1:
        for cannon in eloc:
            bullet = ENEMY.Bullet(cannon[0],cannon[1])
            bull_list.add(bullet)

    #move bullets
    for bullet in bull_list:
        bullet.update()
        #collision detection
        if bullet.rect.y-60 <= player.rect.y <= bullet.rect.y+15:
            if bullet.rect.x-60 <= player.rect.x <= bullet.rect.x+15:
                print("collide") #what to do when collide?
    
    #check for jump
    if player.yspeed >= 0: #if player is falling
        for platform in ploc:
            if  platform[0] - 47 - player.direction <= player.rect.x <=platform[0]+tx*platform[2] - 10 - player.direction and platform[1]-63 <=player.rect.y <= platform[1]-57:
                player.grounded = True

    clock.tick(60) #60 fps limit
    dt = clock.tick(60) / 1000
    player.update(dt)
    player_group.draw(screen)
    pygame.display.update()

pygame.quit()