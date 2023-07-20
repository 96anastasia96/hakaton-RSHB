import pygame
import random
import time
import pygame_menu

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SIZE = 50
OBJECT_SIZE = 30
PLAYER_COLOR = (0, 0, 255)
RIGHT_OBJECT_IMAGE = 'images/tomato.png'
WRONG_OBJECT_IMAGE = 'images/unripe_tomato.png'
BG_COLOR = (255, 255, 255)
FPS = 60


class FallingObject:
    def __init__(self, x, y, image_path, right_object):
        self.x = x
        self.y = y
        # поле, указывающее на то, правильный объект или нет
        self.right_object = right_object
        self.image = pygame.transform.scale(pygame.image.load(image_path), (OBJECT_SIZE, OBJECT_SIZE))

    def move(self):
        self.y += random.randint(1, 5)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x):
        self.x += x

    def draw(self, window):
        pygame.draw.rect(window, PLAYER_COLOR, pygame.Rect(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))


def start_the_game():
    player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - PLAYER_SIZE - 10)
    objects = []
    score = 1
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

        if random.randint(1, 20) == 1:
            if random.randint(1, 2) == 1:
                objects.append(FallingObject(random.randint(OBJECT_SIZE, WINDOW_WIDTH - OBJECT_SIZE), -OBJECT_SIZE,
                                             RIGHT_OBJECT_IMAGE, True))
            else:
                objects.append(FallingObject(random.randint(OBJECT_SIZE, WINDOW_WIDTH - OBJECT_SIZE), -OBJECT_SIZE,
                                             WRONG_OBJECT_IMAGE, False))

        for obj in objects:
            obj.move()
            if pygame.Rect(obj.x, obj.y, OBJECT_SIZE, OBJECT_SIZE).colliderect(
                    pygame.Rect(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE)):
                objects.remove(obj)
                if obj.right_object:
                    score += 1
                else:
                    score -= 1
            elif obj.y > WINDOW_HEIGHT:
                objects.remove(obj)

        # обновление времени здесь
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000

        if seconds >= 60 or score <= 0:
            run = False
            if seconds >= 60:
                final_score_text = font.render(f"Время вышло! Ваш счет: {score}", True, (10, 160, 10))
            else:
                final_score_text = font.render(f"Вы проиграли! Попробуйте еще раз.", True, (10, 160, 10))

        window.fill(BG_COLOR)

        # обновление текста счета
        text = font.render(f'Счет: {score}', 1, (100, 160, 10))
        window.blit(text, (10, 10))

        # Время игры
        total_game_time = 60
        remaining_time = total_game_time - int(seconds)
        game_time = font.render(f'Оставшееся время: {remaining_time}', 1, (100, 160, 10))
        window.blit(game_time, (10, 50))

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
menu = pygame_menu.Menu('Мини-Игра 1', WINDOW_WIDTH, WINDOW_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
menu.add.button('Играть', start_the_game)
menu.mainloop(pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)))