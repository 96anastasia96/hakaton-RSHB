import pygame
import random
import time
import pygame_menu

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SIZE = 50
OBJECT_SIZE = 30
PLAYER = 'images/robot.png'
RIGHT_OBJECT_IMAGE = 'images/tomato.png'
WRONG_OBJECT_IMAGE = 'images/unripe_tomato.png'
WRONG2_OBJECT_IMAGE = 'images/black_tomato.png'
BG_COLOR = (255, 255, 255)
FPS = 60


class FallingObject:
    def __init__(self, x, y, image_path, earn_points):
        self.x = x
        self.y = y
        self.earn_points = earn_points
        self.image = pygame.transform.scale(pygame.image.load(image_path), (OBJECT_SIZE, OBJECT_SIZE))

    def move(self):
        self.y += random.randint(1, 3)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Загрузка изображения игрока
        self.image = pygame.transform.scale(pygame.image.load(PLAYER), (PLAYER_SIZE, PLAYER_SIZE))

    def move(self, x):
        self.x += x

    def draw(self, window):
        # Рисования изображения игрока
        window.blit(self.image, (self.x, self.y))


def start_the_game():
    player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - PLAYER_SIZE - 10)
    objects = []
    score = 1
    vegetables_collected = 0
    run = True
    start_ticks = pygame.time.get_ticks()
    font = pygame.font.Font(None, 36)  # None для использования шрифта по умолчанию
    final_score_text = None

    while run:
        pygame.time.delay(1000 // FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - 5 > 0:
            player.move(-5)
        if keys[pygame.K_RIGHT] and player.x + 5 < WINDOW_WIDTH - PLAYER_SIZE:
            player.move(5)

        rand_object = random.randint(1, 3)
        if random.randint(1, 50) == 1:
            if rand_object == 1:
                objects.append(FallingObject(random.randint(OBJECT_SIZE, WINDOW_WIDTH - OBJECT_SIZE), -OBJECT_SIZE,
                                             RIGHT_OBJECT_IMAGE, 4))
            elif rand_object == 2:
                objects.append(FallingObject(random.randint(OBJECT_SIZE, WINDOW_WIDTH - OBJECT_SIZE), -OBJECT_SIZE,
                                             WRONG_OBJECT_IMAGE, 1))
            else:
                objects.append(FallingObject(random.randint(OBJECT_SIZE, WINDOW_WIDTH - OBJECT_SIZE), -OBJECT_SIZE,
                                             WRONG2_OBJECT_IMAGE, 2))

        for obj in objects:
            obj.move()
            if pygame.Rect(obj.x, obj.y, OBJECT_SIZE, OBJECT_SIZE).colliderect(
                    pygame.Rect(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE)):
                objects.remove(obj)
                score += obj.earn_points
                vegetables_collected += 1
            elif obj.y > WINDOW_HEIGHT:
                objects.remove(obj)

        if vegetables_collected >= 20:
            run = False
            final_score_text = font.render('Ваш счет: ' + str(score * 100), 1, (10, 10, 10))


        window.fill(BG_COLOR)

        # обновление текста счета
        text = font.render(f'Счет: {score}', 1, (100, 160, 10))
        window.blit(text, (10, 10))

        if final_score_text is not None:
            window.blit(final_score_text, (WINDOW_WIDTH // 2 - final_score_text.get_width() // 2, WINDOW_HEIGHT // 2))

        player.draw(window)
        for obj in objects:
            obj.draw(window)
        pygame.display.update()

    window.blit(final_score_text, (WINDOW_WIDTH // 2 - final_score_text.get_width() // 2, WINDOW_HEIGHT // 2))
    pygame.display.flip()
    time.sleep(5)


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
description = 'В этой мини-игре вам нужно управлять роботом и собрать 20 падающих овощей.'
rules = 'За каждый собранный овощ вы получаете очки: зелёный - 2, переспелый - 1, спелый - 4. В конце раунда ваши очки умножаются на 100'
menu = pygame_menu.Menu('Мини-Игра 1', WINDOW_WIDTH, WINDOW_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
menu.add.label(description, max_char=-1, font_size=18)
menu.add.label(rules, max_char=-1, font_size=18)
menu.add.button('Играть', start_the_game)
menu.mainloop(pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)))
