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
BORDO = (155, 0, 50)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('Arial', 23)
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

BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets', 'space.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

BIG_BULLET_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Big_bullet.png')), (20, 20))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_b_bullets, yellow_b_bullets):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BORDO, BORDER)
    red_health_text = HEALTH_FONT.render(
        str(int(red_health))+'%', 1,  WHITE)
    yellow_health_text = HEALTH_FONT.render(
        str(int(yellow_health))+'%', 1, BORDO)

    # red health bars
    pygame.draw.rect(WIN, WHITE, (pygame.Rect(718, 18, 154, 29)))
    pygame.draw.rect(WIN, BLACK, (pygame.Rect(721, 21, 148, 23)))
    pygame.draw.rect(WIN, RED, (pygame.Rect(720, 20, red_health*1.5, 25)))
    #yellow health bars
    pygame.draw.rect(WIN, WHITE, (pygame.Rect(28, 18, 154, 29)))
    pygame.draw.rect(WIN, BLACK, (pygame.Rect(31, 21, 148, 23)))
    pygame.draw.rect(WIN, YELLOW, (pygame.Rect(30, 20, yellow_health * 1.5, 25)))

    WIN.blit(red_health_text, (722, 18))
    WIN.blit(yellow_health_text, (32, 18))


    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in red_b_bullets:
        #pygame.draw.rect(WIN, RED, bullet)
        WIN.blit(BIG_BULLET_IMAGE, (bullet.x, bullet.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in yellow_b_bullets:
        #pygame.draw.rect(WIN, YELLOW, bullet)
        WIN.blit(BIG_BULLET_IMAGE, (bullet.x, bullet.y))

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
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2,
                         HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(800, 230, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 230, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)


    red_bullets = []
    yellow_bullets = []
    yellow_b_bullets = []
    red_b_bullets = []

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
                else:
                    red_health -= 4
                    BULLET_HIT_SOUND.play()
            if event.type == RED_BIG_HIT:
                red_health -= 9
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                crit_chance = random.randrange(1,100)
                if crit_chance in range(0, 11):
                    yellow_health -= 6
                    BULLET_HIT_SOUND.play()
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
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow_b_bullets, red_b_bullets, yellow, red)
        draw_window(
            red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_b_bullets, yellow_b_bullets)

    main()


if __name__ == '__main__':
    main()
