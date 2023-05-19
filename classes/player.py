import pygame
import os
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc):
        pygame.sprite.Sprite.__init__(self, )
        self.direction = 10
        self.gravityConstant = 12.5
        self.jumpForce = 10
        self.yspeed = 0
        self.grounded = True
        jump_path = os.path.join(sys.path[0], "assets", "sprites", "Pirate Bomb", "Sprites", "1-Player-Bomb Guy", "4-Jump")
        self.images = [pygame.image.load(os.path.join(jump_path, f"{i}.png")) for i in range(1, 4)]
        self.image = self.images[0]
        self.rect = pygame.Rect((xloc + 20, yloc), (37, 57))
        self.frame = 0

    def move(self, steps):
        if self.direction != steps: #if there is change in directions
            self.rect.x += steps*2
        self.direction = steps
        self.rect.x += steps

    def jump(self):
        self.yspeed = -self.jumpForce

    def update(self, dt):

        #gravity
        self.yspeed += self.gravityConstant * dt

        #jump
        if self.grounded:
            self.jump()
            self.grounded = False
        
        #move the player down
        self.rect.y += self.yspeed
        if 0 < self.yspeed <= 4:
            self.frame = 1
        elif self.yspeed > 4:
            self.frame = 2
        elif self.yspeed <= 0:
            self.frame = 0

        #left
        if self.direction < 0:
            self.image = pygame.transform.flip(self.images[self.frame], True, False)

        #right
        if self.direction > 0:
            self.image = self.images[self.frame]