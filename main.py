from random import *
import pygame
pygame.init()

clock = pygame.time.Clock()
FPS = 75

screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
bg_image = pygame.image.load('bg.jpg')

spaceship_image = pygame.image.load('spaceship.png')
spaceship_width, spaceship_height = 70, 70
spaceship_image = pygame.transform.scale(spaceship_image, (spaceship_width, spaceship_height))
spaceship_x, spaceship_y = screen_width / 2 - spaceship_width / 2, screen_height - spaceship_height
spaceship_step = 15


bullet_step = 15
bullet_image = pygame.image.load('bullet.png')
bullet_width, bullet_height = 20, 20
bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))
bullets = []

bullet_sound = pygame.mixer.Sound('sound.mp3')
bullet_sound.set_volume(0.2)
pygame.mixer.music.load('bgsound.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

enemy_step = 5
enemy_image = pygame.image.load('enemy.png')
enemy_width, enemy_height = 80, 80
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
enemys = []
for i in range(5):
    enemy_x = randint(0, screen_width - enemy_width)
    enemy_y = -randint(enemy_height, screen_height)
    enemys.append([enemy_x, enemy_y])


def start_game():
    global spaceship_x, spaceship_y, bullets, enemys, score
    spaceship_x, spaceship_y = (
        screen_width / 2 - spaceship_width / 2,
        screen_height - spaceship_height
    )
    bullets = []
    score = 0
    enemys = []
    for i in range(5):
        enemy_x = randint(0, screen_width - enemy_width)
        enemy_y = -randint(enemy_height, screen_height)
        enemys.append([enemy_x, enemy_y])

start_game()




hit_sound = pygame.mixer.Sound('hit_sound.mp3')
hit_sound.set_volume(0.2)

step = 20
score = 0 
font = pygame.font.Font(None, 36)

game_over = False
restart_text = font.render("Press Enter to Continue", True, (13,47,56))
restart_text_rect = restart_text.get_rect(center=(screen_width / 2, screen_height - 50))
exit_text = font.render("Press Esc to quit", True, (13,47,56))
exit_text_rect = exit_text.get_rect(center=(screen_width / 2, screen_height - 25))
exit_text_rect.y -= exit_text_rect.height + 50
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_RETURN:
                if game_over:
                    start_game()
                    game_over = False
            if event.key == pygame.K_SPACE and not game_over:
                bullet_x = spaceship_x + spaceship_width / 2 - bullet_width/ 2
                bullet_y = spaceship_y - bullet_width
                bullets.append([bullet_x, bullet_y])
                bullet_sound.play()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and spaceship_y >= spaceship_step:
        spaceship_y -= spaceship_step
    if keys[pygame.K_DOWN] and spaceship_y <= screen_height - spaceship_height - spaceship_step:
        spaceship_y += spaceship_step
    if keys[pygame.K_LEFT] and spaceship_x >= spaceship_step:
        spaceship_x -= spaceship_step
    if keys[pygame.K_RIGHT] and spaceship_x <= screen_width - spaceship_width - spaceship_step:
        spaceship_x += spaceship_step

    screen.blit(bg_image, (-300, 0))
    if not game_over:
        screen.blit(spaceship_image, (spaceship_x, spaceship_y))

    for i in bullets:
        i[1] -= bullet_step
        if i[1] + bullet_height <= 0:
            bullets.remove(i)
        else:
            screen.blit(bullet_image, (i[0], i[1]))
    

    for i in enemys:
        i[1] += enemy_step 
        if i[1] > screen_height:
            i[0] = randint(0, screen_width - enemy_width)
            i[1] = -enemy_height
    for i in enemys:
        if not game_over:
            screen.blit(enemy_image, (i[0], i[1]))
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
        bullet_mask = pygame.mask.from_surface(bullet_image)
        for enemy in enemys:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            enemy_mask = pygame.mask.from_surface(enemy_image)
            offset = (round(enemy_rect.x - bullet_rect.x), round(enemy_rect.y - bullet_rect.y))
            if bullet_mask.overlap(enemy_mask, offset):
                bullets.remove(bullet)
                enemys.remove(enemy)
                hit_sound.play()
                score += 1
                new_enemy_x= randint(0, screen_width - enemy_width)
                new_enemy_y = -randint (enemy_height, screen_height)
                enemys.append([new_enemy_x, new_enemy_y])
                break

    spaceship_rect = pygame.Rect(spaceship_x, spaceship_y, spaceship_width, spaceship_height)
    for enemy in enemys:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
        if spaceship_rect.colliderect(enemy_rect):
            game_over = True
    if game_over:
        game_over_font = pygame.font.Font(None, 190)
        game_over_text = game_over_font.render('Game over!', True, (255, 255, 255))
        text_rect = game_over_text.get_rect(
            center=(screen_width / 2, screen_height / 2)
        )
        screen. blit (game_over_text, text_rect)
        screen. blit (restart_text, restart_text_rect)
        screen. blit(exit_text, exit_text_rect)
    clock.tick(FPS)
    pygame.display.update()