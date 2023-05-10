import pygame
import os
import sys

#pygame setup
pygame.init()
screen = pygame.display.set_mode((480, 800))
clock = pygame.time.Clock()
running = True
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
sprite_dir = os.path.join(sys.path[0], "assets", "sprites", "Pirate Bomb", "Sprites", "1-Player-Bomb Guy", "1-Idle", "1.png")
player = pygame.image.load(sprite_dir)
while running:
    #event handler
    for event in pygame.event.get():
        #player clicks the X button
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    clock.tick(60) #60 fps limit
    screen.blit(player, player_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_a] and player_pos.x > 0:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d] and player_pos.x < 425:
        player_pos.x += 300 * dt

    pygame.display.update()
    dt = clock.tick(60) / 1000

pygame.quit()