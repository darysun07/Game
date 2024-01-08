import pygame
from pygame import mixer

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from classes.player import Player


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

PINK = (255, 15, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (75, 0, 130)

FPS = 60

ROUND_OVER_COOLDOWN = 2000

WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]


class Yrovni(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/yrovni.ui', self)
        self.lgk_button.clicked.connect(self.lgk_glav_window_opn)
        self.srdn_button.clicked.connect(self.srd_glav_window_opn)
        self.slzn_button.clicked.connect(self.slz_glav_window_opn)

    def lgk_glav_window_opn(self):
        mixer.init()
        pygame.init()

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wild West")

        clock = pygame.time.Clock()

        intro_count = 3
        last_count_update = pygame.time.get_ticks()
        score = [0, 0]
        round_over = False

        pygame.mixer.music.load("assets/audio/music1.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
        sword_fx.set_volume(0.5)
        magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
        magic_fx.set_volume(0.75)

        bg_image = pygame.image.load("assets/images/background/fon2.png").convert_alpha()

        warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
        wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

        victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

        game_over_img = pygame.image.load("assets/images/background/fon6.jpg").convert_alpha()

        count_font = pygame.font.Font("assets/fonts/turok.ttf", 100)
        score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

        def draw_text(text, font, text_col, x, y):
            img = font.render(text, True, text_col)
            screen.blit(img, (x, y))

        def draw_bg():
            scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_bg, (0, 0))

        def draw_health_bar(health, x, y):
            ratio = health / 30
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(screen, PINK, (x, y, 400, 30))
            pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

        player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, 30)
        player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 30)

        run = True
        while run:

            clock.tick(FPS)

            draw_bg()

            draw_health_bar(player_1.health, 60, 20)
            draw_health_bar(player_2.health, 730, 20)
            draw_text("P1: " + str(score[0]), score_font, PINK, 60, 60)
            draw_text("P2: " + str(score[1]), score_font, PINK, 730, 60)

            if intro_count <= 0:
                player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2, round_over)
                player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1, round_over)
            else:
                draw_text(str(intro_count), count_font, PINK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

            player_1.update()
            player_2.update()

            player_1.draw(screen)
            player_2.draw(screen)

            if not round_over:
                if not player_1.alive:
                    score[1] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                elif not player_2.alive:
                    score[0] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
            else:
                screen.blit(victory_img, (500, 300))
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 3
                    player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,
                                      sword_fx, 30)
                    player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 30)

            if score[0] == 3 or score[1] == 3:
                game_over_img = pygame.transform.scale(game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(game_over_img, (0, 0))
                pygame.mixer.music.stop()
                round_over = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
        pygame.quit()

    def srd_glav_window_opn(self):
        mixer.init()
        pygame.init()

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wild West")

        clock = pygame.time.Clock()

        intro_count = 3
        last_count_update = pygame.time.get_ticks()
        score = [0, 0]
        round_over = False

        pygame.mixer.music.load("assets/audio/music2.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
        sword_fx.set_volume(0.5)
        magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
        magic_fx.set_volume(0.75)

        bg_image = pygame.image.load("assets/images/background/fon3.jpg").convert_alpha()

        warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
        wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

        victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

        game_over_img = pygame.image.load("assets/images/background/fon5.jpg").convert_alpha()

        count_font = pygame.font.Font("assets/fonts/turok.ttf", 100)
        score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

        def draw_text(text, font, text_col, x, y):
            img = font.render(text, True, text_col)
            screen.blit(img, (x, y))

        def draw_bg():
            scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_bg, (0, 0))

        def draw_health_bar(health, x, y):
            ratio = health / 70
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(screen, PINK, (x, y, 400, 30))
            pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

        player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, 70)
        player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 70)

        run = True
        while run:

            clock.tick(FPS)

            draw_bg()

            draw_health_bar(player_1.health, 60, 20)
            draw_health_bar(player_2.health, 730, 20)
            draw_text("P1: " + str(score[0]), score_font, BLUE, 60, 60)
            draw_text("P2: " + str(score[1]), score_font, BLUE, 730, 60)

            if intro_count <= 0:
                player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2, round_over)
                player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1, round_over)
            else:
                draw_text(str(intro_count), count_font, BLUE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

            player_1.update()
            player_2.update()

            player_1.draw(screen)
            player_2.draw(screen)

            if not round_over:
                if not player_1.alive:
                    score[1] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                elif not player_2.alive:
                    score[0] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
            else:
                screen.blit(victory_img, (500, 300))
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 3
                    player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,
                                      sword_fx, 70)
                    player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 70)

            if score[0] == 3 or score[1] == 3:
                game_over_img = pygame.transform.scale(game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(game_over_img, (0, 0))
                pygame.mixer.music.stop()
                round_over = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
        pygame.quit()

    def slz_glav_window_opn(self):
        mixer.init()
        pygame.init()

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wild West")

        clock = pygame.time.Clock()

        intro_count = 3
        last_count_update = pygame.time.get_ticks()
        score = [0, 0]
        round_over = False

        pygame.mixer.music.load("assets/audio/music3.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
        sword_fx.set_volume(0.5)
        magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
        magic_fx.set_volume(0.75)

        bg_image = pygame.image.load("assets/images/background/fon4.jpg").convert_alpha()

        warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
        wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

        victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

        game_over_img = pygame.image.load("assets/images/background/fon7.jpg").convert_alpha()

        count_font = pygame.font.Font("assets/fonts/turok.ttf", 100)
        score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

        def draw_text(text, font, text_col, x, y):
            img = font.render(text, True, text_col)
            screen.blit(img, (x, y))

        def draw_bg():
            scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_bg, (0, 0))

        def draw_health_bar(health, x, y):
            ratio = health / 110
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(screen, PINK, (x, y, 400, 30))
            pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

        player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, 110)
        player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 110)

        run = True
        while run:

            clock.tick(FPS)

            draw_bg()

            draw_health_bar(player_1.health, 60, 20)
            draw_health_bar(player_2.health, 730, 20)
            draw_text("P1: " + str(score[0]), score_font, RED, 60, 60)
            draw_text("P2: " + str(score[1]), score_font, RED, 730, 60)

            if intro_count <= 0:
                player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2, round_over)
                player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1, round_over)
            else:
                draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

            player_1.update()
            player_2.update()

            player_1.draw(screen)
            player_2.draw(screen)

            if not round_over:
                if not player_1.alive:
                    score[1] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                elif not player_2.alive:
                    score[0] += 1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
            else:
                screen.blit(victory_img, (500, 300))
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 3
                    player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,
                                      sword_fx, 110)
                    player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 110)

            if score[0] == 3 or score[1] == 3:
                game_over_img = pygame.transform.scale(game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(game_over_img, (0, 0))
                pygame.mixer.music.stop()
                round_over = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
        pygame.quit()