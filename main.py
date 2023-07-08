import pygame
import classes.player as PLAYER
import classes.platform as LEVEL
import classes.enemy as ENEMY
import random
import os
import sys
import neat
import pickle

highscore = 0

#pygame setup
pygame.init()
screen = pygame.display.set_mode((480, 800))
clock = pygame.time.Clock()
pygame.display.set_caption('Dodle Joomp')

#bgm setup
music = pygame.mixer.music.load(os.path.join(sys.path[0], "assets", "sound", "Pirate 3.mp3"))
pygame.mixer.music.play(-1)

def eval_genomes(genomes, config, score):
    for genome_id, genome in genomes:
        genome.fitness = score

def main(genomes, config):
    #clock
    clock.tick(60) #60 fps limit
    dt = clock.tick(60) / 1000

    #game variables
    global highscore
    game_over = 0
    running = True

    #NEAT setup
    players = []
    networks = []
    ge = []
    for id, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        players.append(PLAYER.Player(200, 700))
        genome.fitness = 0
        ge.append(genome)

    #entities setup
    player_group = pygame.sprite.Group()
    plat_list = pygame.sprite.Group()
    enem_list = pygame.sprite.Group()
    bull_list = pygame.sprite.Group()
    player_group.add(players) #might not work
    steps = 10
    tx = ty = 32
    max_platforms = 6
    max_enemies = 6
    pygame.display.set_icon(players[0].image)

    #initialize first entities
    plat_list = LEVEL.platform(0, 800-ty, plat_list, 1, 15)
    enem_list = ENEMY.enemy(random.choice([0,480-30]), 800-196-ty-32, enem_list, 1)
    plat_no = 0

    #background
    background_path = os.path.join(sys.path[0], "assets", "sprites", "background")
    clouds = pygame.sprite.Group()
    for i in range(4):
        cloud = pygame.sprite.Sprite()
        cloud.image =  pygame.image.load(os.path.join(background_path, f"{i}.png")).convert_alpha()
        cloud.rect = cloud.image.get_rect()
        cloud.rect.x = 100 * i
        cloud.rect.y = 700 - 150 *i
        clouds.add(cloud)

    #camera and score
    offset = 0
    curr_score = 0
    font = pygame.font.Font("freesansbold.ttf", 32)
    text_score = font.render(f"Score: {curr_score}", True, (0, 255, 0), (0, 0, 128))
    textRect_score = text_score.get_rect()
    textRect_score.topleft = (0, 0)
    text_hs = font.render(f"Highcore: {curr_score}", True, (0, 255, 0), (0, 0, 128))
    textRect_hs = text_hs.get_rect()
    textRect_hs.topleft = (0, 32)

    while running:
        #event handler
        for event in pygame.event.get():
            #player clicks the X button
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over == 1:
                    main(genomes, config)
        
        #stop when no players remain
        if len(players) <= 0:
            running = False
            return

        #generate platforms
        if plat_no < max_platforms:
            plat_list = LEVEL.platform(random.randint(0,480-tx), plat_list.sprites()[-1].rect.y - 196, plat_list, 1, random.randint(1,9))
            plat_no += 1
        
        #generate cannons
        if len(enem_list.sprites()) < max_enemies:
            enem_list = ENEMY.enemy(random.choice([0,480-30]), enem_list.sprites()[-1].rect.y - 196, enem_list, 1)

        #background
        screen.fill((146, 169, 206))

        #entities
        clouds.draw(screen)
        plat_list.draw(screen)
        enem_list.draw(screen)
        bull_list.draw(screen)

        # #movement
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_a] and player.rect.x > 0:
        #     player.move(-steps)
        # if keys[pygame.K_d] and player.rect.x < 420:
        #     player.move(steps)

        #AI movement
        t_offset = 0
        for id, player in enumerate(players):
            player.update(dt)

            #Ray inputs + player velocity
            input_data = player.detect(plat_list.sprites(), bull_list.sprites())
            input_data.append(player.yspeed)
            input_data.append(player.direction)

            #output
            output = networks[id].activate(input_data)
            action = output.index(max(output))

            #move player based on output
            if action == 0 and player.rect.x > 0:
                player.move(-steps)
            elif action == 1 and player.rect.x < 420:
                player.move(steps)

            #platform collision
            if player.yspeed >= 0: #if player is falling
                for platform in plat_list:
                    if  pygame.sprite.collide_rect(player, platform) and player.rect.y <= platform.rect.y - 40:
                        player.grounded = True

            #camera offset
            platform_removed = False
            if player.rect.y <= 400:
                offset = 400 - player.rect.y
                player.rect.y += offset
                player.score += offset
                ge[id].fitness = player.score
                if player.score > curr_score:
                    curr_score = player.score
                if curr_score > highscore:
                    highscore = curr_score
                if offset > t_offset:
                    t_offset = offset

            #death
            if player.rect.y > 800:
                players.pop(id)
                networks.pop(id)
                ge.pop(id)
                player.die()

        #offset every sprite
        for sprite in plat_list.sprites() + enem_list.sprites() + bull_list.sprites():
            #problem : everything is being offset cuz of every player
            sprite.rect.y += t_offset
            #clear offscreen entities
            if sprite.rect.y > 800:
                if sprite.die() == 0:
                    platform_removed = True

        if platform_removed:
            plat_no -= 1
            
        #shoot bullets
        if len(bull_list) < 1:
            for cannon in enem_list:
                bullet = ENEMY.Bullet(cannon.rect.x, cannon.rect.y)
                bull_list.add(bullet)

        #move bullets
        for bullet in bull_list:
            bullet.update()
            #collision detection
            for id, player in enumerate(players):
                if pygame.sprite.collide_rect(player, bullet):
                    players.pop(id)
                    networks.pop(id)
                    ge.pop(id)
                    player.die()

        #Restart when player dies            
        if player.dead:
            text = font.render("Press R to Respawn", False, (255, 255, 255))
            rect = text.get_rect()
            rect.center = screen.get_rect().center
            screen.blit(text, rect)
            game_over = 1

        #without rays
        player_group.draw(screen)
        #with rays, slow
        # for player in player_group.sprites():
        #     player.draw(screen)
        text = font.render(f"Score: {curr_score}", True, (0, 255, 0), (0, 0, 128))
        screen.blit(text, textRect_score)
        text = font.render(f"Highscore: {highscore}", True, (0, 255, 0), (0, 0, 128))
        screen.blit(text, textRect_hs)
        pygame.display.update()

    pygame.quit()

# run AI
def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    winner = p.run(main)

    with open('winner', 'wb') as f:
        pickle.dump(winner, f)

# run specific AI
def run_genome(config_path, genome_path = "winner"):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    genomes = [(1, genome)]

    run(genomes, config)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.ini")
    run(config_path)

#main()