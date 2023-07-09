import pygame
import os
import sys
import random
import math
from shapely.geometry import Polygon

DEBUGMODE = True
RAY_WIDTH = 2
sys.path.append("..")
sound_dir = [os.path.join(sys.path[0], "assets", "sound", "player", "death.mp3")]
sound_dir += [os.path.join(sys.path[0], "assets", "sound", "player", f"jump{i}.mp3") for i in range(1,4)]

class Player(pygame.sprite.Sprite):
    RAY_SIZE = 200

    def __init__(self, xloc, yloc):
        pygame.sprite.Sprite.__init__(self)
        self.x = xloc
        self.y = yloc
        self.dead = False
        self.direction = 10
        self.gravityConstant = 12.5
        self.jumpForce = 10
        self.yspeed = 0
        self.grounded = True
        jump_path = os.path.join(sys.path[0], "assets", "sprites", "player")
        self.images = [pygame.image.load(os.path.join(jump_path, f"{i}.png")) for i in range(1, 4)]
        self.image = self.images[0]
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect = pygame.Rect((xloc + 20, yloc), (37, 57))
        self.frame = 0
        self.rays = []
        self.rays_collided = []
        self.score = 0

    def move(self, steps):
        if self.direction != steps: #if there is change in directions
            self.rect.x += steps*2
        self.direction = steps
        self.rect.x += steps

    def jump(self):
        pygame.mixer.Sound.play(pygame.mixer.Sound(sound_dir[random.randint(1,3)]))
        self.yspeed = -self.jumpForce

    def update(self, dt):
        if not self.dead:
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

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        self.cast_rays()

        if DEBUGMODE:
            for i, rays in enumerate(self.rays):
                for ray in rays:
                    color = (75, 50, 255)

                    if self.rays_collided and self.rays_collided[i] > 0:
                        color = (35, 255, 0)
                    elif self.rays_collided and self.rays_collided[i] < 0:
                        color = (255, 35, 0)

                    pygame.draw.polygon(screen, color, ray.exterior.coords, 2)

    def cast_rays(self):
        self.rays = [
            # Top top right
            [Polygon([
                (self.rect.x + self.width + (self.RAY_SIZE * 0.3), self.rect.y - (self.RAY_SIZE * 0.8)),
                (self.rect.x + self.width + (self.RAY_SIZE * 0.3) - RAY_WIDTH, self.rect.y - (self.RAY_SIZE * 0.8)),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2) + RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
            ])],
            # Top right right
            [Polygon([
                (self.rect.x + self.width + (self.RAY_SIZE * 0.8), self.rect.y + (self.height / 2) - (self.RAY_SIZE * 0.65)),
                (self.rect.x + self.width + (self.RAY_SIZE * 0.8), self.rect.y + (self.height / 2) - (self.RAY_SIZE * 0.65) - RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2) + RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
            ])],
            # Right
            [Polygon([
                (self.rect.x + self.width + self.RAY_SIZE, self.rect.y + (self.height / 2)),
                (self.rect.x + self.width + self.RAY_SIZE, self.rect.y + (self.height / 2) + RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2) + RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
            ])],
            # Bottom right right
            [Polygon([
                (self.rect.x + self.width + (self.RAY_SIZE * 0.8), self.rect.y + (self.height / 2) + (self.RAY_SIZE * 0.65)),
                (self.rect.x + self.width + (self.RAY_SIZE * 0.8), self.rect.y + (self.height / 2) + (self.RAY_SIZE * 0.65) - RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2) + RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
            ])],
            # Bottom bottom right
            [Polygon([
                (self.rect.x + self.width + (self.RAY_SIZE * 0.3), self.rect.y + self.height + (self.RAY_SIZE * 0.8)),
                (self.rect.x + self.width + (self.RAY_SIZE * 0.3) - RAY_WIDTH, self.rect.y + self.height + (self.RAY_SIZE * 0.8)),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2) + RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
            ])],
            # Bottom
            [Polygon([
                (self.rect.x + (self.width / 2) - (RAY_WIDTH / 2), self.rect.y + self.height + self.RAY_SIZE),
                (self.rect.x + (self.width / 2) - (RAY_WIDTH / 2), self.rect.y + (self.height / 2)),
                (self.rect.x + (self.width / 2) + (RAY_WIDTH / 2), self.rect.y + (self.height / 2)),
                (self.rect.x + (self.width / 2) + (RAY_WIDTH / 2), self.rect.y + self.height + self.RAY_SIZE)
            ])],
            # Bottom bottom left
            [Polygon([
                (self.rect.x - (self.RAY_SIZE * 0.3), self.rect.y + self.height + (self.RAY_SIZE * 0.8)),
                (self.rect.x - (self.RAY_SIZE * 0.3) - RAY_WIDTH, self.rect.y + self.height + (self.RAY_SIZE * 0.8)),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2) + RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
            ])],
            # Bottom left left
            [Polygon([
                (self.rect.x - (self.RAY_SIZE * 0.8), self.rect.y + (self.height / 2) + (self.RAY_SIZE * 0.65)),
                (self.rect.x - (self.RAY_SIZE * 0.8), self.rect.y + (self.height / 2) + (self.RAY_SIZE * 0.65) - RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2) + RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
            ])],
            # Left
            [Polygon([
                (self.rect.x - self.RAY_SIZE, self.rect.y + (self.height / 2)),
                (self.rect.x - self.RAY_SIZE, self.rect.y + (self.height / 2) + RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2) + RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
            ])],
            # Left left top
            [Polygon([
                (self.rect.x - (self.RAY_SIZE * 0.8), self.rect.y + (self.height / 2) - (self.RAY_SIZE * 0.65)),
                (self.rect.x - (self.RAY_SIZE * 0.8), self.rect.y + (self.height / 2) - (self.RAY_SIZE * 0.65) - RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2) + RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
            ])],
            # Left top top
            [Polygon([
                (self.rect.x - (self.RAY_SIZE * 0.3), self.rect.y - (self.RAY_SIZE * 0.8)),
                (self.rect.x - (self.RAY_SIZE * 0.3) - RAY_WIDTH, self.rect.y - (self.RAY_SIZE * 0.8)),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2) + RAY_WIDTH),
                (self.rect.x + (self.width / 2), self.rect.y + (self.height / 2))
            ])],
            # Top
            [Polygon([
                (self.rect.x + (self.width / 2) - (RAY_WIDTH / 2), self.rect.y - self.RAY_SIZE),
                (self.rect.x + (self.width / 2) - (RAY_WIDTH / 2), self.rect.y + (self.height / 2)),
                (self.rect.x + (self.width / 2) + (RAY_WIDTH / 2), self.rect.y + (self.height / 2)),
                (self.rect.x + (self.width / 2) + (RAY_WIDTH / 2), self.rect.y - self.RAY_SIZE)
            ])]
        ]

    def die(self):
        pygame.mixer.Sound.play(pygame.mixer.Sound(sound_dir[0]))
        self.kill()
        self.rect.x = 1000
        self.rect.y = 400
        self.dead = True
        return True   
    
    def check_collision_platform(self, plat_list):
        if self.yspeed >= 0: #if player is falling
            for platform in plat_list:
                if  self.rect.colliderect(platform.rect):
                    self.grounded = True
                    #print(self.rays_collided) # just for checking

    def detect(self, plat_list, bull_list):
        self.rays_collided = []

        if self.rays:
            for rays in self.rays:
                cast = False
                for i, bullet in enumerate(bull_list):
                    for ray in rays:
                        if ray.intersects(bullet.polygon) and not cast:
                            self.rays_collided.append(-round(math.dist((self.rect.x + self.width/2, self.rect.y + self.height/2), bullet.position)))
                            cast = True
                
                for i, platform in enumerate(plat_list):
                    for ray in rays:
                        if ray.intersects(platform.polygon) and not cast:
                            self.rays_collided.append(round(math.dist((self.rect.x + self.width/2, self.rect.y + self.height/2), platform.position)))
                            cast = True
                if not cast:
                    self.rays_collided.append(0)
        else:
            self.rays_collided = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            return self.rays_collided

        return self.rays_collided 
        #array showing distance of object from player (-ve if bullet, +ve if platform). ordered starting from 1-o'clock hand to 12-o'clock