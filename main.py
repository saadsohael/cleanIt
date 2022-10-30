import random
import pygame
import math
from sys import exit
import os


# saving high score in a text file
def save_high_score(new_score):
    global highScore

    try:
        with open('scores/high_score.txt', 'r') as scoreFile:
            high_score = scoreFile.read()

        if new_score > int(high_score):
            with open('scores/high_score.txt', 'w') as scoreFile:
                scoreFile.write(str(new_score))
                highScore = new_score

    except FileNotFoundError:
        with open('scores/high_score.txt', 'w') as scoreFile:
            scoreFile.write(str(new_score))
            highScore = new_score


# getting window information
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Construct the GUI game
pygame.init()

# Creating a clock
clock = pygame.time.Clock()

# Set variables and initial values
angle = 0
start_time = 0
game_started = False
game_over = False
game_paused = False
tank_flipped = False
fired_state = False
shooting = False
collecting = True
spawn_at_a_time_increased = False
collect_water_bottle = False
target_pos = pygame.mouse.get_pos()
pygame.mouse.set_visible(False)

# setting logo
logo = pygame.image.load('logo.png')
pygame.display.set_icon(logo)

# Set dimensions of game GUI
window_info = pygame.display.Info()
screen_width, screen_height = window_info.current_w, window_info.current_h
game_screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# bgs
bg_floor = pygame.image.load('graphics/floor.jpeg').convert_alpha()
bg_floor = pygame.transform.scale(bg_floor, (screen_width, screen_height))

menu_bg = pygame.image.load('graphics/menu_screen.png').convert_alpha()
menu_bg = pygame.transform.scale(menu_bg, (screen_width, screen_height))

# menu screen text
start_hover = False
how_to_play_hover = False
exit_hover = False

menu_text_font = pygame.font.Font('fonts/Li Alinur Kurigram Unicode.ttf', 48)
start_text = menu_text_font.render('START', False, 'Black')
start_text_rect = start_text.get_rect(center=((screen_width // 2 - start_text.get_width() // 2 + 20),
                                              (screen_height // 2 - start_text.get_height() // 2 - 150)))

how_to_play = menu_text_font.render('HOW TO PLAY', False, 'Black')
how_to_play_rect = how_to_play.get_rect(center=((screen_width // 2 - start_text.get_width() // 2 + 20),
                                                (screen_height // 2 - start_text.get_height() // 2)))

exit_text = menu_text_font.render('EXIT', False, 'Black')
exit_text_rect = exit_text.get_rect(center=((screen_width // 2 - start_text.get_width() // 2 + 20),
                                            (screen_height // 2 - start_text.get_height() // 2 + 150)))

# short instruction
instruction_font = pygame.font.Font('fonts/Li Alinur Kurigram Unicode.ttf', 48)
instruction_text = instruction_font.render('Press Tab To Change To Shooting Mode', False, 'Red')
instruction_shown = False

# health
health = [99, 85, 68, 51, 37, 25, 17, 10, 0]
health_font = pygame.font.Font('fonts/Caveat-Bold.ttf', 42)

# Water Tank
tank_width = 120
tank_height = 80
tank_x = screen_width // 2
tank_y = screen_height // 2

tank = pygame.image.load(f"graphics/tank_sprites/tank_{health[-1]}.png").convert_alpha().convert_alpha()
tank = pygame.transform.scale(tank, (tank_width, tank_height))
tank_rect = tank.get_rect(center=(tank_x, tank_y))

# Shooter
shooter_width = 20
shooter_height = 80
shooter = pygame.image.load('graphics/shooter.png').convert_alpha()
shooter = pygame.transform.scale(shooter, (shooter_width, shooter_height))
shooter.convert()

# Store the image in a new variable
# Construct the rectangle around image
img = shooter
rect = img.get_rect()

# water / weapon
water_width = 30
water_height = 30
shoot_speed = 15
water = pygame.image.load('graphics/weapon.png').convert_alpha()
water = pygame.transform.scale(water, (water_width, water_height))
water_rect = water.get_rect(center=tank_rect.center)

# collectable water bottle
water_bottle = pygame.image.load('graphics/water_bottle.png').convert_alpha()
water_bottle = pygame.transform.scale(water_bottle, (20, 40))
water_bottle_list = []
bottle_collecting_speed = 25

# bullet/ water left
water_left = []
for v in range(0, 250, 50):
    water_left.append(water.get_rect(center=(40 + v, 40)))

# creating aim
aim_width = 40
aim_height = 40
aim = pygame.transform.scale(pygame.image.load('graphics/aim.png').convert_alpha(), (aim_width, aim_height))
aim_rect = aim.get_rect(center=(screen_width // 2, screen_height // 2))

# enemies
enemy_width = 60
enemy_height = 60
enemy_speed = 4
enemy = pygame.image.load('graphics/enemy.png').convert_alpha()
enemy = pygame.transform.scale(enemy, (enemy_width, enemy_height))

enemy_list = []
spawn_at_a_time = 1

# dead sprite of enemy (dead hagu)
dead_hagu = pygame.image.load('graphics/dead_hagu.png').convert_alpha()
dead_hagu = pygame.transform.scale(dead_hagu, (enemy_width, enemy_height))
dead_hagu_list = []

# custom events
enemy_spawn_event = pygame.USEREVENT + 1
enemy_spawn_time = 1400
pygame.time.set_timer(enemy_spawn_event, enemy_spawn_time)

# modes
mode_width = 100
mode_height = 60
collecting_mode = pygame.transform.scale(pygame.image.load('graphics/collecting_mode.png').convert_alpha(),
                                         (mode_width, mode_height))
shooting_mode = pygame.transform.scale(pygame.image.load('graphics/shooting_mode.png').convert_alpha(),
                                       (mode_width, mode_height))

# scoring
score = 0
score_font = pygame.font.Font('fonts/COPRGTB.TTF', 24)

# high score
try:
    with open('scores/high_score.txt', 'r') as HighScoreFile:
        highScore = HighScoreFile.read()
except FileNotFoundError:
    highScore = 0

# game over design
enemy_image_w = 150
enemy_image_h = 150
enemy_image = pygame.transform.scale((pygame.image.load('graphics/enemy.png').convert_alpha()),
                                     (enemy_image_w, enemy_image_h))

# musics
bg_music = pygame.mixer.Sound('sounds/the-great-battle.mp3')
bg_music.set_volume(0.6)

bullet_sound = pygame.mixer.Sound('sounds/bullet-sound.wav')
bullet_sound.set_volume(0.6)

drag_bottle_sound = pygame.mixer.Sound('sounds/drag-bottle.wav')
drag_bottle_sound.set_volume(0.7)

death_sound = pygame.mixer.Sound('sounds/death-sound.wav')
death_sound.set_volume(0.4)
death_sound_played = False

menu_music = pygame.mixer.Sound('sounds/menu-music.mp3')
menu_music.set_volume(0.6)
menu_music.play(-1)
menu_music_playing = False

# pause screen texts
resume_hover = False
restart_hover = False
back_to_menu_hover = False
pause_surface = pygame.Surface((800, 400))
resume_text = menu_text_font.render('RESUME', False, 'Black', 'Red')
resume_rect = resume_text.get_rect(midtop=(screen_width // 2, screen_height // 2 - 150))
restart_text = menu_text_font.render('RESTART', False, 'Black', 'Red')
restart_rect = restart_text.get_rect(midtop=(screen_width // 2, screen_height // 2 - 50))
back_to_menu_text = menu_text_font.render('END GAME', False, 'Black', 'Red')
back_to_menu_rect = back_to_menu_text.get_rect(center=(screen_width // 2, screen_height // 2 + 80))

# how to play screen
instruction_screen = False
how_to_play_screen = pygame.image.load('graphics/howToPlay3.png').convert_alpha()
how_to_play_screen = pygame.transform.scale(how_to_play_screen, (screen_width, screen_height))

if __name__ == "__main__":

    # Setting what happens when game is in running state
    while True:

        if game_paused and pygame.mouse.get_pressed()[0]:
            if resume_hover:
                game_paused = False

            if restart_hover:
                bg_music.stop()
                start_time = pygame.time.get_ticks()
                enemy_list.clear()
                dead_hagu_list.clear()
                score = 0
                spawn_at_a_time = 1
                enemy_speed = 4
                spawn_at_a_time_increased = False
                shooting = False
                collecting = True
                game_paused = False
                instruction_shown = False

                health = [99, 85, 68, 51, 37, 25, 17, 10, 0]

                water_left.clear()
                for v in range(0, 250, 50):
                    water_left.append(water.get_rect(center=(40 + v, 40)))
                water_bottle_list.clear()
                collect_water_bottle = False

                tank = pygame.image.load(
                    f"graphics/tank_sprites/tank_{health[-1]}.png").convert_alpha().convert_alpha()
                tank = pygame.transform.scale(tank, (tank_width, tank_height))
                tank_rect = tank.get_rect(center=(tank_x, tank_y))

                if not tank_flipped:
                    midbottom = tank_rect.centerx, tank_rect.centery - shooter_height * 1 / 4

                else:
                    midbottom = (tank_rect.left + tank_width // 2, tank_rect.top + 110)

                if tank_flipped:
                    tank = pygame.transform.flip(tank, flip_x=False, flip_y=True)
                    img = pygame.transform.flip(shooter, flip_x=False, flip_y=True)
                    rect = img.get_rect()
                    rect.midbottom = midbottom
                    if not fired_state:
                        water_rect.center = tank_rect.center
                    tank_rect = tank.get_rect(center=(tank_x, tank_y))
                    tank_flipped = False

                game_over = False
                bg_music.play(-1)
                death_sound_played = False

            elif back_to_menu_hover:
                bg_music.fadeout(1)
                if not menu_music_playing:
                    menu_music.play(-1)
                    menu_music_playing = True
                game_started = False

        if game_started and not game_over and not game_paused:
            if not fired_state and pygame.mouse.get_pressed()[0]:
                target_pos = pygame.mouse.get_pos()
                if water_left and shooting:
                    if not tank_flipped and target_pos[1] <= tank_rect.top - 10:
                        bullet_sound.play()
                        fired_state = True
                        water_left.pop()
                    elif tank_flipped and target_pos[1] >= tank_rect.bottom + 10:
                        bullet_sound.play()
                        fired_state = True
                        water_left.pop()

                if water_bottle_list and collecting:
                    for water_bottle_rectangle in water_bottle_list:
                        if water_bottle_rectangle.collidepoint(target_pos):
                            if water_bottle_rectangle.centery > tank_rect.centery and tank_flipped:
                                drag_bottle_sound.play()
                                collect_water_bottle = True
                            elif water_bottle_rectangle.centery < tank_rect.centery and not tank_flipped:
                                drag_bottle_sound.play()
                                collect_water_bottle = True

        # common events loop
        for event in pygame.event.get():

            # Close if the user quits the game
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEMOTION:
                if game_started:
                    # if game started but now paused
                    if game_paused:
                        if resume_rect.collidepoint(event.pos):
                            resume_hover = True
                        elif restart_rect.collidepoint(event.pos):
                            restart_hover = True
                        elif back_to_menu_rect.collidepoint(event.pos):
                            back_to_menu_hover = True
                        else:
                            resume_hover = False
                            restart_hover = False
                            back_to_menu_hover = False

                    # if game started and not paused
                    else:
                        if not tank_flipped:
                            midbottom = tank_rect.centerx, tank_rect.centery - shooter_height * 1 / 4

                        else:
                            midbottom = (tank_rect.left + tank_width // 2, tank_rect.top + 110)

                        rect.midbottom = midbottom
                        # Move the image with the specified coordinates, angle and scale
                        mouse = event.pos
                        x = mouse[0] - midbottom[0]
                        y = mouse[1] - midbottom[1]
                        angle = math.degrees(-math.atan2(y, -x))

                        if not tank_flipped:
                            if 25 < angle < 155:
                                img = pygame.transform.rotate(shooter, (90 - angle))
                                rect = img.get_rect()
                                rect.midbottom = midbottom
                                if not fired_state:
                                    water_rect = water.get_rect(center=tank_rect.center)

                        else:
                            if -150 < angle < -26:
                                img = pygame.transform.rotate(shooter, (90 - angle))
                                rect = img.get_rect()
                                rect.midbottom = midbottom
                                if not fired_state:
                                    water_rect = water.get_rect(center=tank_rect.center)

                # when mouse moving in menu screen
                else:
                    if start_text_rect.collidepoint(event.pos):
                        start_hover = True
                    elif how_to_play_rect.collidepoint(event.pos):
                        how_to_play_hover = True
                    elif exit_text_rect.collidepoint(event.pos):
                        exit_hover = True
                    else:
                        start_hover = False
                        how_to_play_hover = False
                        exit_hover = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if not game_started:

                    if start_hover:

                        game_started = True
                        start_time = pygame.time.get_ticks()
                        enemy_list.clear()
                        dead_hagu_list.clear()
                        score = 0
                        spawn_at_a_time = 1
                        enemy_speed = 4
                        spawn_at_a_time_increased = False
                        shooting = False
                        collecting = True
                        game_paused = False
                        menu_music_playing = False
                        instruction_shown = False

                        health = [99, 85, 68, 51, 37, 25, 17, 10, 0]

                        water_left.clear()
                        for v in range(0, 250, 50):
                            water_left.append(water.get_rect(center=(40 + v, 40)))
                        water_bottle_list.clear()
                        collect_water_bottle = False

                        tank = pygame.image.load(
                            f"graphics/tank_sprites/tank_{health[-1]}.png").convert_alpha().convert_alpha()
                        tank = pygame.transform.scale(tank, (tank_width, tank_height))
                        tank_rect = tank.get_rect(center=(tank_x, tank_y))

                        if not tank_flipped:
                            midbottom = tank_rect.centerx, tank_rect.centery - shooter_height * 1 / 4

                        else:
                            midbottom = (tank_rect.left + tank_width // 2, tank_rect.top + 110)

                        rect.midbottom = midbottom

                        if tank_flipped:
                            tank = pygame.transform.flip(tank, flip_x=False, flip_y=True)
                            img = pygame.transform.flip(shooter, flip_x=False, flip_y=True)
                            rect = img.get_rect()
                            rect.midbottom = midbottom
                            if not fired_state:
                                water_rect.center = tank_rect.center
                            tank_rect = tank.get_rect(center=(tank_x, tank_y))
                            tank_flipped = False

                        game_over = False
                        menu_music.fadeout(1)
                        bg_music.play(-1)
                        death_sound_played = False

                    elif how_to_play_hover:
                        instruction_screen = True
                    elif exit_hover:
                        exit()

            if event.type == pygame.KEYDOWN:
                if game_started:

                    if not tank_flipped:
                        midbottom = tank_rect.centerx, tank_rect.centery - shooter_height * 1 / 4

                    else:
                        midbottom = (tank_rect.left + tank_width // 2, tank_rect.top + 110)

                    rect.midbottom = midbottom

                    if not game_over:

                        if event.key == pygame.K_SPACE and not tank_flipped and not game_paused:
                            tank = pygame.transform.flip(tank, flip_x=False, flip_y=True)
                            img = pygame.transform.flip(shooter, flip_x=False, flip_y=True)
                            rect = img.get_rect()
                            rect.midbottom = midbottom
                            if not fired_state:
                                water_rect.center = tank_rect.center
                            tank_rect = tank.get_rect(center=(tank_x, tank_y))
                            tank_flipped = True

                        elif event.key == pygame.K_SPACE and tank_flipped and not game_paused:
                            tank = pygame.transform.flip(tank, flip_x=False, flip_y=True)
                            img = pygame.transform.flip(shooter, flip_x=False, flip_y=True)
                            img = pygame.transform.rotate(img, 180)
                            rect = img.get_rect()
                            rect.midbottom = midbottom

                            if not fired_state:
                                water_rect.center = tank_rect.center
                            tank_rect = tank.get_rect(center=(tank_x, tank_y))

                            tank_flipped = False

                        elif event.key == pygame.K_TAB and not game_paused:
                            if shooting:
                                collecting = True
                                shooting = False
                            elif collecting:
                                shooting = True
                                collecting = False
                            if not instruction_shown:
                                instruction_shown = True

                        elif event.key == pygame.K_ESCAPE:
                            if not game_paused:
                                game_paused = True
                            else:
                                game_paused = False

                    elif game_over:

                        if event.key == pygame.K_r:

                            start_time = pygame.time.get_ticks()
                            enemy_list.clear()
                            dead_hagu_list.clear()
                            score = 0
                            spawn_at_a_time = 1
                            enemy_speed = 4
                            spawn_at_a_time_increased = False
                            shooting = False
                            collecting = True
                            game_paused = False
                            instruction_shown = False

                            health = [99, 85, 68, 51, 37, 25, 17, 10, 0]

                            water_left.clear()
                            for v in range(0, 250, 50):
                                water_left.append(water.get_rect(center=(40 + v, 40)))
                            water_bottle_list.clear()
                            collect_water_bottle = False

                            tank = pygame.image.load(
                                f"graphics/tank_sprites/tank_{health[-1]}.png").convert_alpha().convert_alpha()
                            tank = pygame.transform.scale(tank, (tank_width, tank_height))
                            tank_rect = tank.get_rect(center=(tank_x, tank_y))

                            if tank_flipped:
                                tank = pygame.transform.flip(tank, flip_x=False, flip_y=True)
                                img = pygame.transform.flip(shooter, flip_x=False, flip_y=True)
                                rect = img.get_rect()
                                rect.midbottom = midbottom
                                if not fired_state:
                                    water_rect.center = tank_rect.center
                                tank_rect = tank.get_rect(center=(tank_x, tank_y))
                                tank_flipped = False

                            game_over = False
                            bg_music.play(-1)
                            death_sound_played = False

                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if instruction_screen:
                                instruction_screen = False

            # spawning enemies
            if event.type == enemy_spawn_event and not game_paused and instruction_shown:
                for v in range(spawn_at_a_time):
                    random_x = random.randint(-200, screen_width + 200)
                    random_y = random.choice([-150, -150, screen_height + 150])
                    enemy_rect = enemy.get_rect(center=(random_x, random_y))
                    enemy_list.append(enemy_rect)

                if dead_hagu_list:
                    dead_hagu_list.remove(dead_hagu_list[0])

        if game_started:

            if not health:

                if not death_sound_played:
                    death_sound.play()
                    death_sound_played = True
                bg_music.fadeout(1)
                game_over = True
                save_high_score(score)

            if fired_state:

                bullet_move_distance = pygame.Vector2(target_pos) - pygame.Vector2(water_rect.center)
                bullet_move_length = bullet_move_distance.length()

                if bullet_move_length < shoot_speed:
                    water_rect.center = target_pos
                elif bullet_move_length != 0:
                    bullet_move_distance.normalize_ip()
                    bullet_move_distance = bullet_move_distance * shoot_speed
                    water_rect.center += bullet_move_distance
                if water_rect.center == target_pos:
                    water_rect.center = tank_rect.center
                    target_pos = tank_rect.center
                    fired_state = False

            if enemy_list:

                for enemy_rectangle in enemy_list:

                    if not game_over and not game_paused:

                        # enemy movement
                        enemy_move_distance = pygame.Vector2(tank_rect.center) - pygame.Vector2(enemy_rectangle.center)
                        enemy_move_length = enemy_move_distance.length()

                        if enemy_move_length < enemy_speed:
                            enemy_rectangle.center = tank_rect.center

                        elif enemy_move_length != 0:
                            enemy_move_distance.normalize_ip()
                            enemy_move_distance = enemy_move_distance * enemy_speed
                            enemy_rectangle.center += enemy_move_distance

                    # killing enemies conditions
                    if water_rect.colliderect(enemy_rectangle) and not game_over:
                        water_rect.center = tank_rect.center
                        fired_state = False
                        score += 1
                        dead_hagu_list.append(dead_hagu.get_rect(center=enemy_rectangle.center))
                        enemy_list.remove(enemy_rectangle)

                    # game over conditions
                    if health:
                        try:
                            if enemy_rectangle.colliderect(rect) or enemy_rectangle.colliderect(tank_rect):
                                health.pop()
                                if health:
                                    tank = pygame.image.load(
                                        f"graphics/tank_sprites/tank_{health[-1]}.png").convert_alpha().convert_alpha()
                                    tank = pygame.transform.scale(tank, (tank_width, tank_height))
                                    tank_rect = tank.get_rect(center=(tank_x, tank_y))
                                enemy_list.remove(enemy_rectangle)
                        except ValueError:
                            pass

            if water_bottle_list:

                for bottle_rectangle in water_bottle_list:

                    if not game_over and collect_water_bottle:

                        # bottle movement
                        bottle_move_distance = pygame.Vector2(tank_rect.center) - pygame.Vector2(
                            bottle_rectangle.center)
                        bottle_move_length = bottle_move_distance.length()

                        if bottle_move_length < bottle_collecting_speed:
                            bottle_rectangle.center = tank_rect.center

                        elif bottle_move_length != 0:
                            bottle_move_distance.normalize_ip()
                            bottle_move_distance = bottle_move_distance * bottle_collecting_speed
                            bottle_rectangle.center += bottle_move_distance

                    if tank_rect.colliderect(bottle_rectangle) and len(water_left) != 5:
                        water_left.clear()
                        for v in range(0, 250, 50):
                            water_left.append(water.get_rect(center=(40 + v, 40)))
                        water_bottle_list.clear()
                        collect_water_bottle = False

            if not tank_flipped:
                midbottom = tank_rect.centerx, tank_rect.centery - shooter_height * 1 / 4

            else:
                midbottom = (tank_rect.left + tank_width // 2, tank_rect.top + 110)

            rect.midbottom = midbottom

            # Set screen color and images on screen
            game_screen.blit(bg_floor, (0, 0))

            # bottle spawn
            if random.choice(
                    [len(water_left) <= 2, len(water_left) <= 2, len(water_left) <= 3, len(water_left) == 1]) and len(
                water_bottle_list) == 0 and not game_paused:
                random_x = random.choice([random.randint(10, (tank_rect.topleft[0] - 5)),
                                          random.randint((tank_rect.topright[0] + 5), (screen_width - 10))])
                random_y = random.choice(
                    [random.randint(10, tank_rect.top - 10), random.randint(tank_rect.bottom + 10, screen_height - 10)])
                # print(f'water y pos: {random_y}')
                water_bottle_rect = water_bottle.get_rect(center=(random_x, random_y))
                water_bottle_list.append(water_bottle_rect)

            if not game_over:

                # drawing running game stuffs on screen

                if not instruction_shown:
                    game_screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2,
                                                        screen_height - instruction_text.get_height() - 10))

                    # water bottles
                if water_bottle_list:
                    for v in water_bottle_list:
                        game_screen.blit(water_bottle, v)

                # water left
                if water_left:
                    game_screen.blit(water, water_rect)

                game_screen.blit(img, rect)

                if health:
                    game_screen.blit(tank, tank_rect)

                score_text = score_font.render(f'Cleaned : {score}', False, 'Black')
                game_screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

                for drop in water_left:
                    game_screen.blit(water, drop)

                # health bar
                if health:
                    if health[-1] <= 60:
                        health_text = health_font.render(f'{health[-1]}% Shitty', False, 'Black')
                    elif 60 < health[-1] <= 85:
                        health_text = health_font.render(f'{health[-1]}% Shitty', False, 'Orange')
                    else:
                        health_text = health_font.render(f'{health[-1]}% Shitty', False, 'Red')

                    game_screen.blit(health_text,
                                     (health_text.get_width(), screen_height - health_text.get_height() - 50))

                if enemy_list:
                    for enemy_rectangle in enemy_list:
                        game_screen.blit(enemy, enemy_rectangle)

                if dead_hagu_list:
                    for dead_hagu_rect in dead_hagu_list:
                        game_screen.blit(dead_hagu, dead_hagu_rect)

                # shooting or collecting modes
                if shooting:
                    game_screen.blit(shooting_mode,
                                     ((screen_width - mode_width - 15), (screen_height - mode_height - 15)))
                else:
                    game_screen.blit(collecting_mode,
                                     ((screen_width - mode_width - 15), (screen_height - mode_height - 15)))

            if game_over:
                # drawing the game over screen
                game_screen.blit(enemy_image,
                                 (screen_width // 2 - enemy_image_w // 2, screen_height // 2 - enemy_image_h - 80))

                score_text = score_font.render(f'Total {score} MrHagu Cleaned!', False, 'Black')
                game_screen.blit(score_text, (
                    screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - score_text.get_height() // 2))

                highScore_text = score_font.render(f'High Score : {highScore}', False, 'Black')
                game_screen.blit(highScore_text, (screen_width // 2 - highScore_text.get_width() // 2,
                                                  screen_height // 2 - highScore_text.get_height() // 2 + 50))

                start_again_text = score_font.render('Press R To Start Again!', False, 'Red')
                game_screen.blit(start_again_text, (screen_width // 2 - start_again_text.get_width() // 2,
                                                    screen_height // 2 - start_again_text.get_height() // 2 + 150))

            # speeding up enemy spawn
            if score > 5 and (
                    (pygame.time.get_ticks() - start_time) // 1000) % 20 == 0 and not spawn_at_a_time_increased:
                spawn_at_a_time += 1
                enemy_speed -= 1
                if spawn_at_a_time > 3:
                    spawn_at_a_time = 1
                    enemy_speed = 4

                spawn_at_a_time_increased = True

            if ((pygame.time.get_ticks() - start_time) // 1000) % 20 != 0 and spawn_at_a_time_increased:
                spawn_at_a_time_increased = False

        if game_paused:

            pause_surface.fill('Blue')
            pause_surface.set_alpha(100)
            game_screen.blit(pause_surface, (screen_width // 2 - 400, screen_height // 2 - 200))

            if resume_hover:
                resume_text = menu_text_font.render('RESUME', False, 'Black', 'Red')
                game_screen.blit(resume_text, resume_rect)

                restart_text = menu_text_font.render('RESTART', False, 'Black')
                game_screen.blit(restart_text, restart_rect)

                back_to_menu_text = menu_text_font.render('END GAME', False, 'Black')
                game_screen.blit(back_to_menu_text, back_to_menu_rect)

            if restart_hover:

                restart_text = menu_text_font.render('RESTART', False, 'Black', 'Red')
                game_screen.blit(restart_text, restart_rect)

                resume_text = menu_text_font.render('RESUME', False, 'Black')
                game_screen.blit(resume_text, resume_rect)

                back_to_menu_text = menu_text_font.render('END GAME', False, 'Black')
                game_screen.blit(back_to_menu_text, back_to_menu_rect)

            elif back_to_menu_hover:

                back_to_menu_text = menu_text_font.render('END GAME', False, 'Black', 'Red')
                game_screen.blit(back_to_menu_text, back_to_menu_rect)

                resume_text = menu_text_font.render('RESUME', False, 'Black')
                game_screen.blit(resume_text, resume_rect)

                restart_text = menu_text_font.render('RESTART', False, 'Black')
                game_screen.blit(restart_text, restart_rect)

            else:

                resume_text = menu_text_font.render('RESUME', False, 'Black')
                game_screen.blit(resume_text, resume_rect)
                restart_text = menu_text_font.render('RESTART', False, 'Black')
                game_screen.blit(restart_text, restart_rect)
                back_to_menu_text = menu_text_font.render('END GAME', False, 'Black')
                game_screen.blit(back_to_menu_text, back_to_menu_rect)

            # darken the screen
            dark = pygame.Surface((bg_floor.get_width(), bg_floor.get_height()), flags=pygame.SRCALPHA)
            dark.fill((10, 10, 10, 80))
            game_screen.blit(dark, (0, 0))

        if not game_started:

            if not instruction_screen:
                game_screen.blit(menu_bg, (0, 0))
            else:
                game_screen.blit(how_to_play_screen, (0, 0))

            if start_hover and not instruction_screen:

                menu_text_font = (pygame.font.Font('fonts/Li Alinur Kurigram Unicode.ttf', 60))
                start_ = pygame.draw.rect(game_screen, 'Blue', (
                    start_text_rect[0] - 30, start_text_rect[1] - 10, start_text_rect[2] + 60, start_text_rect[3] + 20),
                                          0, 25)
                start_text = menu_text_font.render('START', False, 'White')
                game_screen.blit(start_text, (start_[0] + 15, start_[1], start_[2], start_[3]))

                menu_text_font = (pygame.font.Font('fonts/Li Alinur Kurigram Unicode.ttf', 48))
                pygame.draw.rect(game_screen, 'Blue', (
                    how_to_play_rect[0] - 25, how_to_play_rect[1], how_to_play_rect[2] + 50, how_to_play_rect[3] + 5,),
                                 5, 25)
                how_to_play = menu_text_font.render('HOW TO PLAY', False, 'Black')
                game_screen.blit(how_to_play, how_to_play_rect)

                menu_text_font = (pygame.font.Font('fonts/Li Alinur Kurigram Unicode.ttf', 48))
                pygame.draw.rect(game_screen, 'Blue', (
                    exit_text_rect[0] - 25, exit_text_rect[1], exit_text_rect[2] + 50, exit_text_rect[3] + 5,), 5, 25)
                exit_text = menu_text_font.render('EXIT', False, 'Black')
                game_screen.blit(exit_text, exit_text_rect)

            elif how_to_play_hover and not instruction_screen:

                menu_text_font = (pygame.font.Font('fonts/Li Alinur Kurigram Unicode.ttf', 60))
                how_to_play_ = pygame.draw.rect(game_screen, 'Blue', (
                    how_to_play_rect[0] - 60, how_to_play_rect[1] - 10, how_to_play_rect[2] + 120,
                    how_to_play_rect[3] + 20), 0, 25)

                how_to_play = menu_text_font.render('HOW TO PLAY', False, 'White')
                game_screen.blit(how_to_play, (
                    how_to_play_[0] + 22, how_to_play_[1] + 2, how_to_play_[2], how_to_play_[3]))

                menu_text_font = (pygame.font.Font('fonts/Li Alinur Kurigram Unicode.ttf', 48))
                pygame.draw.rect(game_screen, 'Blue', (
                    start_text_rect[0] - 25, start_text_rect[1], start_text_rect[2] + 50, start_text_rect[3] + 5,), 5,
                                 25)
                start_text = menu_text_font.render('START', False, 'Black')
                game_screen.blit(start_text, start_text_rect)

                menu_text_font = (pygame.font.Font('fonts/Li Alinur Kurigram Unicode.ttf', 48))
                pygame.draw.rect(game_screen, 'Blue', (
                    exit_text_rect[0] - 25, exit_text_rect[1], exit_text_rect[2] + 50, exit_text_rect[3] + 5,), 5, 25)
                exit_text = menu_text_font.render('EXIT', False, 'Black')
                game_screen.blit(exit_text, exit_text_rect)

            elif exit_hover and not instruction_screen:

                menu_text_font = (pygame.font.Font('fonts/Li Alinur Kurigram Unicode.ttf', 60))
                exit_ = pygame.draw.rect(game_screen, 'Blue',
                                         (exit_text_rect[0] - 30, exit_text_rect[1] - 10, exit_text_rect[2] + 60,
                                          exit_text_rect[3] + 20), 0, 25)
                exit_text = menu_text_font.render('EXIT', False, 'White')
                game_screen.blit(exit_text, (exit_[0] + 20, exit_[1], exit_[2], exit_[3]))

                menu_text_font = (pygame.font.Font('fonts/Li Alinur Kurigram Unicode.ttf', 48))
                pygame.draw.rect(game_screen, 'Blue', (
                    start_text_rect[0] - 25, start_text_rect[1], start_text_rect[2] + 50, start_text_rect[3] + 5,), 5,
                                 25)
                start_text = menu_text_font.render('START', False, 'Black')
                game_screen.blit(start_text, start_text_rect)

                menu_text_font = (pygame.font.Font('fonts/Li Alinur Kurigram Unicode.ttf', 48))
                pygame.draw.rect(game_screen, 'Blue', (
                    how_to_play_rect[0] - 25, how_to_play_rect[1], how_to_play_rect[2] + 50, how_to_play_rect[3] + 5,),
                                 5, 25)
                how_to_play = menu_text_font.render('HOW TO PLAY', False, 'Black')
                game_screen.blit(how_to_play, how_to_play_rect)

            else:
                if not instruction_screen:
                    pygame.draw.rect(game_screen, 'Blue', (
                        start_text_rect[0] - 25, start_text_rect[1], start_text_rect[2] + 50, start_text_rect[3] + 5,),
                                     5, 25)
                    start_text = menu_text_font.render('START', False, 'Black')
                    game_screen.blit(start_text, start_text_rect)

                    pygame.draw.rect(game_screen, 'Blue', (
                        how_to_play_rect[0] - 25, how_to_play_rect[1], how_to_play_rect[2] + 50,
                        how_to_play_rect[3] + 5,),
                                     5, 25)
                    how_to_play = menu_text_font.render('HOW TO PLAY', False, 'Black')
                    game_screen.blit(how_to_play, how_to_play_rect)

                    pygame.draw.rect(game_screen, 'Blue', (
                        exit_text_rect[0] - 25, exit_text_rect[1], exit_text_rect[2] + 50, exit_text_rect[3] + 5,), 5,
                                     25)
                    exit_text = menu_text_font.render('EXIT', False, 'Black')
                    game_screen.blit(exit_text, exit_text_rect)

        # print(spawn_at_a_time, enemy_speed)
        # print(len(water_left))
        # drawing cursor or aim
        aim_rect.center = pygame.mouse.get_pos()
        game_screen.blit(aim, aim_rect)
        # Update the GUI game
        pygame.display.update()
        clock.tick(60)
