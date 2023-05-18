import pygame
import classes.player as PLAYER
import classes.platform as LEVEL
import classes.enemy as ENEMY
import random

#pygame setup
pygame.init()
screen = pygame.display.set_mode((480, 800))
clock = pygame.time.Clock()
running = True

#entities setup
player = PLAYER.Player(0, 700)
player_group = pygame.sprite.Group()
plat_list = pygame.sprite.Group()
enem_list = pygame.sprite.Group()
bull_list = pygame.sprite.Group()
player_group.add(player)
steps = 10
tx = ty = 32
max_platforms = 6
max_enemies = 4

#camera
max_height = 0
offset = 0

#initialize first entities
plat_list = LEVEL.platform(0, 800-ty, plat_list, 1, 15)
enem_list = ENEMY.enemy(random.choice([0,480-30]), 800-196-ty-32, enem_list, 1)
plat_no = 1
enemy_no = 1

while running:
    #event handler
    for event in pygame.event.get():
        #player clicks the X button
        if event.type == pygame.QUIT:
            running = False
    
    #generate platforms
    if plat_no < max_platforms:
        plat_list = LEVEL.platform(random.randint(0,480-tx), plat_list.sprites()[-1].rect.y - 196, plat_list, 1, random.randint(1,9))
        plat_no += 1
    #generate cannons
    if enemy_no < max_enemies:
        enem_list = ENEMY.enemy(random.choice([0,480-30]), enem_list.sprites()[-1].rect.y - 196, enem_list, 1)
        enemy_no += 1

    screen.fill((0, 0, 0))
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
        for cannon in enem_list:
            bullet = ENEMY.Bullet(cannon.rect.x, cannon.rect.y)
            bull_list.add(bullet)

    #move bullets
    for bullet in bull_list:
        bullet.update()
        #collision detection
        if bullet.rect.y-60 <= player.rect.y <= bullet.rect.y+15:
            if bullet.rect.x-60 <= player.rect.x <= bullet.rect.x+15:
                print("collide") #what to do when collide?
    
    #platform collision
    if player.yspeed >= 0: #if player is falling
        for platform in plat_list:
            if  platform.rect.x-47-player.direction <= player.rect.x <=platform.rect.x+tx-10-player.direction and platform.rect.y-63<=player.rect.y <= platform.rect.y-57:
                player.grounded = True

    #camera offset
    entity_removed = [False, False, False]
    if player.rect.y <= 400:
        offset = 400 - player.rect.y
        #offset every sprite
        for sprite in plat_list.sprites() + enem_list.sprites() + bull_list.sprites() + player_group.sprites():
            sprite.rect.y += offset
            #clear offscreen entities
            if sprite.rect.y > 800:
                entity_removed[sprite.die()] = True
        if entity_removed[0]:
            plat_no -= 1
        if entity_removed[1]:
            enemy_no -= 1

    if player.rect.y > 800:
        player.kill()
        print("GAME OVER")
    
    clock.tick(60) #60 fps limit
    dt = clock.tick(60) / 1000
    player.update(dt)
    player_group.draw(screen)
    pygame.display.update()

pygame.quit()

#Things to do:
#Improve collision (use the functions pygame actually gives us)
#Figure out how to remove unused objects from memory