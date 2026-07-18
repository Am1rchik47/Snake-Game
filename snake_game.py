# Если что я джун и мне было лень разбивать все на файлы. Извините! 
import pygame
import random
import os
pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake-game')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
lose_font = pygame.font.SysFont(None, 100)
lose_text = lose_font.render("Ты проиграл(", True, (255, 255, 255))

# Змейка
snake_x = 380
snake_y = 280
snake_size = 20
snake_length = 1
snake_body = []
change_x = 0
change_y = 0

# Яблоко
# Скрытая математика чтобы яблоко было по сетке
apple_center_x = random.randint(0, 39) * 20
apple_center_y = random.randint(0, 29) * 20
apple_radius = 10

# Игровой счет и рекорд
score = 0
highscore = 0

# Загрузка рекорда
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TO_FILE = os.path.join(BASE_DIR, "highscore.txt")
if os.path.exists(PATH_TO_FILE):
    with open(PATH_TO_FILE, "r") as file:
        highscore = int(file.read())

game_over = False

# Игровой цикл
while True:
    # Движение змейки
    snake_x += change_x
    snake_y += change_y

    # Запись движения
    snake_head = [snake_x, snake_y]
    snake_body.append(snake_head)
    if len(snake_body) > snake_length:
        del snake_body[0]

    # Проверка на касание границ
    if snake_x >= 800 or snake_x < 0 or snake_y >= 600 or snake_y < 0:
        game_over = True
        change_x = 0
        change_y = 0
        # Побитие рекорда
        if score > highscore:
            highscore = score
            with open(PATH_TO_FILE, "w") as file:
                file.write(str(highscore))

    # Логика съедания яблока
    if abs(snake_x - apple_center_x) <= 15 and abs(snake_y - apple_center_y) <= 15:
        apple_center_x = random.randint(0, 39) * 20
        apple_center_y = random.randint(0, 29) * 20
        score += 1
        snake_length += 1
    
    # Игровое окно
    window.fill((0, 0, 0))

    # Отображаем текст
    score_text = font.render(f"Счет: {score}", True, (255, 255, 255))
    text_highscore = font.render(f"Рекорд: {highscore}", True, (255, 255, 255))
    window.blit(score_text, (20, 20))
    window.blit(text_highscore, (20, 50))

    # Отображаем змейку
    for segment in snake_body:
        pygame.draw.rect(window, (0, 255, 0), (segment[0] + 1, segment[1] + 1, snake_size - 2, snake_size - 2))

    # Отображаем яблоко
    pygame.draw.circle(window, (255, 0, 0), (apple_center_x + 10, apple_center_y + 10), apple_radius)

    # Отображение проигрыша
    if game_over:
        window.fill((64, 64, 64))
        window.blit(score_text, (20, 20))
        window.blit(text_highscore, (20, 50))
        window.blit(lose_text, (180, 250))

    # Проверка событий
    for event in pygame.event.get():
        # Выход
        if event.type == pygame.QUIT:
            print(f"Конечный рекорд: {score}")
            pygame.quit()
            exit()
        # Управление
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                change_x = -5
                change_y = 0
            if event.key == pygame.K_s:
                change_x = 0
                change_y = 5
            if event.key == pygame.K_d:
                change_x = 5
                change_y = 0
            if event.key == pygame.K_w:
                change_x = 0
                change_y = -5

    pygame.display.flip()
    clock.tick(60)