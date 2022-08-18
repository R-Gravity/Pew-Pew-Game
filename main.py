import pygame
import os
import sys
import random
pygame.init()
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pew Pew Game')


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAROON = (155, 0, 50)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (137, 238, 240)

BORDER = pygame.Rect(WIDTH//2 - 2, 0, 4, HEIGHT)
BORDER_FIELD = pygame.Rect(WIDTH//2 - 4, 0, 8, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('Arial', 23)
GAME_FONT = pygame.font.SysFont('Sans', 50)
WINNER_FONT = pygame.font.SysFont('Arial', 100)

FPS = 60
VEL = 5
BULLET_VEL = 10
BIG_BULLET_VEL = 20
MAX_BULLETS = 3
MAX_B_BULLETS = 1
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 55

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
RED_BIG_HIT = pygame.USEREVENT + 3
YELLOW_BIG_HIT = pygame.USEREVENT + 4

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 270)

BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets', 'space1.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

BIG_BULLET_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Big_bullet.png')), (20, 20))
CRIT_HIT_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Crit_hit.png')), (30, 30))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health,
                yellow_health, red_b_bullets, yellow_b_bullets, red_crit_hit, yellow_crit_hit):
    
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, CYAN, BORDER_FIELD)
    pygame.draw.rect(WIN, MAROON, BORDER)

    red_health_text = HEALTH_FONT.render(
        str(int(red_health))+'%', True,  WHITE)
    yellow_health_text = HEALTH_FONT.render(
        str(int(yellow_health))+'%', True, MAROON)
   
    # red health bars
    pygame.draw.rect(WIN, WHITE, (pygame.Rect(718, 18, 154, 29)))
    pygame.draw.rect(WIN, BLACK, (pygame.Rect(721, 21, 148, 23)))
    pygame.draw.rect(WIN, (200, 0, 50), (pygame.Rect(720, 20, red_health*1.5, 25)))
    # yellow health bars
    pygame.draw.rect(WIN, WHITE, (pygame.Rect(28, 18, 154, 29)))
    pygame.draw.rect(WIN, BLACK, (pygame.Rect(31, 21, 148, 23)))
    pygame.draw.rect(WIN, (245, 197, 28), (pygame.Rect(30, 20, yellow_health * 1.5, 25)))

    WIN.blit(red_health_text, (724, 20))
    WIN.blit(yellow_health_text, (34, 20))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in red_b_bullets:
        WIN.blit((pygame.transform.rotate(BIG_BULLET_IMAGE, 180)), (bullet.x, bullet.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in yellow_b_bullets:
        WIN.blit(BIG_BULLET_IMAGE, (bullet.x, bullet.y))
    
    # displaying critical hits
    for hit in red_crit_hit:
        WIN.blit(CRIT_HIT_IMAGE, (red.x, red.y))        
        red_crit_hit.remove(hit)
    for hit in yellow_crit_hit:
        WIN.blit(CRIT_HIT_IMAGE, (yellow.x, yellow.y))        
        yellow_crit_hit.remove(hit)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x > 0:  # left for yellow
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x < 405:  # right for yellow
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y > 0:  # up for yellow
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y < 445:  # down for yellow
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x > 455:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x < 860:  # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y > 0:  # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y < 445:  # down
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow_b_bullets, red_b_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in yellow_b_bullets:
        bullet.x += BIG_BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_BIG_HIT))
            yellow_b_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_b_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
    for bullet in red_b_bullets:
        bullet.x -= BIG_BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_BIG_HIT))
            red_b_bullets.remove(bullet)
        elif bullet.x < 0:
            red_b_bullets.remove(bullet)


def draw_winner(text):
    instruction = 'Press Space to Restart'
    WIN.blit(BACKGROUND, (0, 0))
    draw_text = WINNER_FONT.render(text, True, WHITE)
    draw_instr = HEALTH_FONT.render(instruction, True, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2,
                         HEIGHT//2 - draw_text.get_height()//2))
    WIN.blit(draw_instr, (WIDTH//2 - draw_instr.get_width()//2,
                          400))
    pygame.display.update()
    pygame.time.delay(100)


def main_menu():
    game_name = 'SHOOT THE MOTHERFUCKER!'
    instruction = 'Press Space to Start'
    pos_x = 350
    pos_y = 350
    down_slide = True

    clock = pygame.time.Clock()
    menu_true = True
    while menu_true:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_true = False

# the instruction text jumping up and down, open to refactoring when i'm better.
        if pos_y == 400:
            down_slide = False
        elif pos_y == 350:
            down_slide = True

        if down_slide:
            pos_y += 1
        else:
            pos_y -= 1

        WIN.blit(BACKGROUND, (0, 0))
        draw_game_name = GAME_FONT.render(game_name, True, CYAN)
        draw_instr = HEALTH_FONT.render(instruction, True, WHITE)
        WIN.blit(draw_game_name, (120, 200))
        WIN.blit(draw_instr, (pos_x, pos_y))


        pygame.display.update()


def main():
    red = pygame.Rect(800, 229, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 230, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    yellow_b_bullets = []
    red_b_bullets = []
    red_crit_hit = []
    yellow_crit_hit = []
    crit_frame = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    red_health = 100
    yellow_health = 100

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    main_menu()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_h and len(yellow_b_bullets) < MAX_B_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 10)
                    yellow_b_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RALT and len(red_b_bullets) < MAX_B_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 10)
                    red_b_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                crit_chance = random.randrange(1, 100)
                if crit_chance in range(0, 11):
                    red_health -= 6
                    BULLET_HIT_SOUND.play()
                    red_crit_hit += crit_frame
                else:
                    red_health -= 4
                    BULLET_HIT_SOUND.play()
            if event.type == RED_BIG_HIT:
                red_health -= 9
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                crit_chance = random.randrange(1, 100)
                if crit_chance in range(0, 11):
                    yellow_health -= 6
                    BULLET_HIT_SOUND.play()
                    yellow_crit_hit += crit_frame
                else:
                    yellow_health -= 4
                    BULLET_HIT_SOUND.play()
            if event.type == YELLOW_BIG_HIT:
                yellow_health -= 9
                BULLET_HIT_SOUND.play()            

        winner_text = ''
        if red_health <= 0:
            winner_text = 'YELLOW WINS!'

        if yellow_health <= 0:
            winner_text = 'RED WINS!'

        if winner_text != '':
            draw_winner(winner_text)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = False



        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow_b_bullets, red_b_bullets, yellow, red)
        draw_window(
            red, yellow, red_bullets, yellow_bullets, red_health, yellow_health,
            red_b_bullets, yellow_b_bullets, red_crit_hit, yellow_crit_hit)

    main()


if __name__ == '__main__':
    main_menu()
    main()
