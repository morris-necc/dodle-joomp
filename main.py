import pygame
import classes.player as PLAYER

#pygame setup
pygame.init()
screen = pygame.display.set_mode((480, 800))
clock = pygame.time.Clock()
running = True
player = PLAYER.Player()
player.rect.x = 0
player.rect.y = 700
player_group = pygame.sprite.Group()
player_group.add(player)
steps = 10
while running:
    #event handler
    for event in pygame.event.get():
        #player clicks the X button
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.rect.x > 0:
        player.move(-steps)
    if keys[pygame.K_d] and player.rect.x < 420:
        player.move(steps)

    
    clock.tick(60) #60 fps limit
    dt = clock.tick(60) / 1000
    player.update(dt)
    player_group.draw(screen)
    pygame.display.update()

pygame.quit()