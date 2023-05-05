import pygame

#pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    #event handler
    for event in pygame.event.get():
        #player clicks the X button
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60) #60 fps limit
    
    #Hi lim!
    #Don't worry I haven't started on anything
    #I haven't even read the docs
    #For now I've just copy/pasted the basic setup from the pygame docs

pygame.quit()