import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Задать параметры игры
GAME_TIME = 40  # игра длится 40 секунд
BUG_APPEARANCE_TIME = 100  # появление насекомых
GAME_REWARD = 150  # базовая награда за игру
bug_data = []  # данные о насекомых

# Инициализация
pygame.init()
screen = pygame.display.set_mode((800, 600))

font = pygame.font.Font(None, 36)

# Загрузка изображений
background_img = pygame.image.load('background.png')
bug_img = pygame.image.load('bug.png')
bug_img = pygame.transform.scale(bug_img, (50, 50))  # Устанавливает размер жука на 50x50 пикселей

# Запуск таймера
start_ticks = pygame.time.get_ticks()


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(WHITE)
        text = font.render("Добро пожаловать в Мини-игру 2! Нажмите пробел чтобы начать.", True, BLACK)
        screen.blit(text, [0, 300])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            intro = False

        pygame.display.update()


def show_result(reward):
    screen.fill(WHITE)
    result_text = font.render("Игра окончена! Вы заработали {} монет".format(reward), True, BLACK)
    screen.blit(result_text, (60, 300))
    pygame.display.update()
    pygame.time.wait(3000)


def play_game():
    GAME_REWARD = 150
    start_ticks = pygame.time.get_ticks()
    while (pygame.time.get_ticks() - start_ticks) < GAME_TIME * 1000:
        remaining_time = GAME_TIME - (pygame.time.get_ticks() - start_ticks) // 1000

        # Проверить, нужно ли добавить насекомое
        if (pygame.time.get_ticks() - start_ticks) % BUG_APPEARANCE_TIME == 0:
            bug_x = random.randint(38, 762)
            bug_y = random.randint(38, 562)
            bug_time = pygame.time.get_ticks()
            bug_data.append((bug_x, bug_y, bug_time))

        # Отрисовка фона
        screen.blit(background_img, (0, 0))

        # Удаление насекомых, которые присутствуют на экране в течение 2 секунд
        bug_data[:] = [bug for bug in bug_data if pygame.time.get_ticks() - bug[2] < 2000]

        # Отрисовка насекомых
        for loc in bug_data:
            screen.blit(bug_img, (loc[0], loc[1]))

        for event in pygame.event.get():
            # Проверка кликов мыши для отпугивания насекомых
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for loc in bug_data:
                    if abs(x - loc[0]) < 50 and abs(y - loc[1]) < 50:
                        bug_data.remove(loc)
                        GAME_REWARD += 3

        # Оставшееся время
        time_text = font.render("Осталось: {} секунд".format(remaining_time), True, BLACK)
        screen.blit(time_text, (600, 0))

        # Очки
        score_text = font.render("Очки: {}".format(GAME_REWARD), True, BLACK)
        screen.blit(score_text, (10, 0))  # Позиция установлена в верхний левый угол экрана

        pygame.display.update()
    return GAME_REWARD


def main():
    game_intro()
    reward = play_game()
    show_result(reward)
    pygame.quit()


if __name__ == "__main__":
    main()

