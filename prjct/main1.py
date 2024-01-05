import sys
import pygame
from pygame import mixer
from player import Player
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMessageBox

import sqlite3


class LoginDb:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def is_table(self, table_name):
        query = "SELECT name from sqlite_master WHERE type='table' AND name='{}';".format(table_name)
        cursor = self.conn.execute(query)
        result = cursor.fetchone()
        if result is None:
            return False
        else:
            return True


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('wild_west.ui', self)

        self.loginDb = LoginDb('login.db')
        if self.loginDb.is_table('USERS'):
            pass
        else:
            self.loginDb.conn.execute("CREATE TABLE USERS(NAME TEXT NOT NULL,PASSWORD TEXT)")
            self.loginDb.conn.execute("INSERT INTO USERS VALUES(?, ?)",
                                            ('admin', 'admin'))
            self.loginDb.conn.commit()
        self.enter_btn.clicked.connect(self.loginCheck)
        self.signup_btn.clicked.connect(self.signup_window_opn)
        self.pravila.clicked.connect(self.pravila_window_opn)

    def yrvn_window_opn(self):
        self.yrovni_window_opn = Yrovni()
        self.yrovni_window_opn.show()
    #     mixer.init()
    #     pygame.init()
    #
    #     # create game window
    #     SCREEN_WIDTH = 1200
    #     SCREEN_HEIGHT = 700
    #
    #     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #     pygame.display.set_caption("Wild West")
    #
    #     # set framerate
    #     clock = pygame.time.Clock()
    #     FPS = 60
    #
    #     # define colours
    #     RED = (255, 15, 192)
    #     GREEN = (0, 255, 0)
    #     WHITE = (255, 255, 255)
    #
    #     # define game variables
    #     intro_count = 3
    #     last_count_update = pygame.time.get_ticks()
    #     score = [0, 0]  # player scores. [P1, P2]
    #     round_over = False
    #     ROUND_OVER_COOLDOWN = 2000
    #
    #     # define fighter variables
    #     WARRIOR_SIZE = 162
    #     WARRIOR_SCALE = 4
    #     WARRIOR_OFFSET = [72, 56]
    #     WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
    #     WIZARD_SIZE = 250
    #     WIZARD_SCALE = 3
    #     WIZARD_OFFSET = [112, 107]
    #     WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
    #
    #     # load music and sounds
    #     pygame.mixer.music.load("assets/audio/music.mp3")
    #     pygame.mixer.music.set_volume(0.5)
    #     pygame.mixer.music.play(-1, 0.0, 5000)
    #     sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
    #     sword_fx.set_volume(0.5)
    #     magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
    #     magic_fx.set_volume(0.75)
    #
    #     # load background image
    #     bg_image = pygame.image.load("assets/images/background/fon2.png").convert_alpha()
    #
    #     start_im = pygame.image.load("assets/images/background/fon.jpg").convert_alpha()
    #
    #     # load spritesheets
    #     warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
    #     wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
    #
    #     # load vicory image
    #     victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()
    #
    #     game_over_img = pygame.image.load("GameOver.png").convert_alpha()
    #
    #     # define number of steps in each animation
    #     WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
    #     WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
    #
    #     FLAG = False
    #
    #     # define font
    #     count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
    #     score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
    #
    #     def start_screen():
    #         scaled_st = pygame.transform.scale(start_im, (SCREEN_WIDTH, SCREEN_HEIGHT))
    #         screen.blit(scaled_st, (0, 0))
    #
    #     # function for drawing text
    #     def draw_text(text, font, text_col, x, y):
    #         img = font.render(text, True, text_col)
    #         screen.blit(img, (x, y))
    #
    #     # function for drawing background
    #     def draw_bg():
    #         scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    #         screen.blit(scaled_bg, (0, 0))
    #
    #     # function for drawing fighter health bars
    #     def draw_health_bar(health, x, y):
    #         ratio = health / 100
    #         pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    #         pygame.draw.rect(screen, RED, (x, y, 400, 30))
    #         pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))
    #
    #     # create two instances of fighters
    #     player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    #     player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
    #
    #     # game loop
    #     run = True
    #     while run:
    #
    #         clock.tick(FPS)
    #
    #         start_screen()
    #
    #         # draw background
    #         draw_bg()
    #
    #         # show player stats
    #         draw_health_bar(player_1.health, 60, 20)
    #         draw_health_bar(player_2.health, 730, 20)
    #         draw_text("P1: " + str(score[0]), score_font, RED, 60, 60)
    #         draw_text("P2: " + str(score[1]), score_font, RED, 730, 60)
    #
    #         # update countdown
    #         if intro_count <= 0:
    #             # move fighters
    #             player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2, round_over)
    #             player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1, round_over)
    #         else:
    #             # display count timer
    #             draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    #             # update count timer
    #             if (pygame.time.get_ticks() - last_count_update) >= 1000:
    #                 intro_count -= 1
    #                 last_count_update = pygame.time.get_ticks()
    #
    #         # update fighters
    #         player_1.update()
    #         player_2.update()
    #
    #         # draw fighters
    #         player_1.draw(screen)
    #         player_2.draw(screen)
    #
    #         # check for player defeat
    #         if not round_over:
    #             if not player_1.alive:
    #                 score[1] += 1
    #                 round_over = True
    #                 round_over_time = pygame.time.get_ticks()
    #             elif not player_2.alive:
    #                 score[0] += 1
    #                 round_over = True
    #                 round_over_time = pygame.time.get_ticks()
    #         else:
    #             # display victory image
    #             screen.blit(victory_img, (500, 300))
    #             if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
    #                 round_over = False
    #                 intro_count = 3
    #                 player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,
    #                                   sword_fx)
    #                 player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
    #
    #         if score[0] == 3 or score[1] == 3:
    #             screen.blit(game_over_img, (500, 300))
    #             round_over = True
    #
    #         # event handler
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 run = False
    #
    #         # update display
    #         pygame.display.update()
    #
    #     # exit pygame
    #     pygame.quit()

    def signup_window_opn(self):
        self.signup_window_opn = Signup()
        self.signup_window_opn.show()
        self.close()

    def pravila_window_opn(self):
        self.pravila_window_opn = Pravila()
        self.pravila_window_opn.show()
        self.close()

    def loginCheck(self):
        name = self.name_check.text()
        password = self.password_check.text()
        if (not name) or (not password):
            err_msg = QMessageBox.information(self, 'Внимание!', 'Не все поля заполнены.')
            return err_msg

        rslt = self.loginDb.conn.execute("SELECT * FROM USERS WHERE NAME = ? AND PASSWORD = ?", (name, password))
        if len(rslt.fetchall()):
            self.close()
            self.yrvn_window_opn()
            self.loginDb.conn.close()
        else:
            err_msg = QMessageBox.information(self, 'Внимание!', 'Неправильное имя пользователя или пароль.')
            return err_msg


class Signup(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.reg_btn.clicked.connect(self.insertData)

        self.loginDb = LoginDb('login.db')

    def insertData(self):
        name = self.name_save.text()
        password = self.password_save.text()

        if (not name) or (not password):
            err_msg = QMessageBox.information(self, 'Внимание!', 'Не все поля заполнены.')
            return err_msg

        rslt = self.loginDb.conn.execute("SELECT * FROM USERS WHERE NAME = ?", (name,))

        if rslt.fetchall():
            err_msg = QMessageBox.information(self, 'Внимание!', 'Пользоватеть с таким именем уже зарегистрирован.')
            return err_msg

        else:
            self.loginDb.conn.execute("INSERT INTO USERS VALUES(?, ?)", (name, password))
            self.loginDb.conn.commit()
            self.home_window_opn = Home()
            self.home_window_opn.show()
            self.close()



class Pravila(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pravila.ui', self)


class Yrovni(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('yrovni.ui', self)
        self.lgk_button.clicked.connect(self.lgk_glav_window_opn)
        self.srdn_button.clicked.connect(self.srd_glav_window_opn)
        self.slzn_button.clicked.connect(self.slz_glav_window_opn)

    def lgk_glav_window_opn(self):
        mixer.init()
        pygame.init()

        # create game window
        SCREEN_WIDTH = 1200
        SCREEN_HEIGHT = 700

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wild West")

        # set framerate
        clock = pygame.time.Clock()
        FPS = 60

        # define colours
        RED = (255, 15, 192)
        GREEN = (0, 255, 0)
        WHITE = (255, 255, 255)

        # define game variables
        intro_count = 3
        last_count_update = pygame.time.get_ticks()
        score = [0, 0]  # player scores. [P1, P2]
        round_over = False
        ROUND_OVER_COOLDOWN = 2000

        # define fighter variables
        WARRIOR_SIZE = 162
        WARRIOR_SCALE = 4
        WARRIOR_OFFSET = [72, 56]
        WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
        WIZARD_SIZE = 250
        WIZARD_SCALE = 3
        WIZARD_OFFSET = [112, 107]
        WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
# тута музыка и звуки в легком уровне надо еще фоны найти и поменять кнопки... также разное снятие хп сделать (я сделала), остановку вижу молодец) но надо продумать еще полное закрытие фона или вовсе вылет и игры и окошка выбора уровня
        # load music and sounds
        pygame.mixer.music.load("assets/audio/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
        sword_fx.set_volume(0.5)
        magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
        magic_fx.set_volume(0.75)

        # load background image
        bg_image = pygame.image.load("assets/images/background/fon2.png").convert_alpha()

        start_im = pygame.image.load("assets/images/background/fon.jpg").convert_alpha()

        # load spritesheets
        warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
        wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

        # load vicory image
        victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

        game_over_img = pygame.image.load("GameOver.png").convert_alpha()

        # define number of steps in each animation
        WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
        WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

        FLAG = False

        # define font
        count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
        score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

        def start_screen():
            scaled_st = pygame.transform.scale(start_im, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_st, (0, 0))

        # function for drawing text
        def draw_text(text, font, text_col, x, y):
            img = font.render(text, True, text_col)
            screen.blit(img, (x, y))

        # function for drawing background
        def draw_bg():
            scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_bg, (0, 0))

        # function for drawing fighter health bars
        def draw_health_bar(health, x, y):
            ratio = health / 30
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(screen, RED, (x, y, 400, 30))
            pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

        # create two instances of fighters
        player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, 30)
        player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 30)

        # game loop
        run = True
        while run:

            clock.tick(FPS)

            start_screen()

            # draw background
            draw_bg()

            # show player stats
            draw_health_bar(player_1.health, 60, 20)
            draw_health_bar(player_2.health, 730, 20)
            draw_text("P1: " + str(score[0]), score_font, RED, 60, 60)
            draw_text("P2: " + str(score[1]), score_font, RED, 730, 60)

            # update countdown
            if intro_count <= 0:
                # move fighters
                player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2, round_over)
                player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1, round_over)
            else:
                # display count timer
                draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                # update count timer
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

            # update fighters
            player_1.update()
            player_2.update()

            # draw fighters
            player_1.draw(screen)
            player_2.draw(screen)

            # check for player defeat
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
                # display victory image
                screen.blit(victory_img, (500, 300))
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 3
                    player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,
                                      sword_fx, 30)
                    player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 30)

            if score[0] == 3 or score[1] == 3:
                screen.blit(game_over_img, (500, 300))
                round_over = True

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # update display
            pygame.display.update()

        # exit pygame
        pygame.quit()

    def srd_glav_window_opn(self):
        mixer.init()
        pygame.init()

        # create game window
        SCREEN_WIDTH = 1200
        SCREEN_HEIGHT = 700

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wild West")

        # set framerate
        clock = pygame.time.Clock()
        FPS = 60

        # define colours
        RED = (255, 15, 192)
        GREEN = (0, 255, 0)
        WHITE = (255, 255, 255)

        # define game variables
        intro_count = 3
        last_count_update = pygame.time.get_ticks()
        score = [0, 0]  # player scores. [P1, P2]
        round_over = False
        ROUND_OVER_COOLDOWN = 2000

        # define fighter variables
        WARRIOR_SIZE = 162
        WARRIOR_SCALE = 4
        WARRIOR_OFFSET = [72, 56]
        WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
        WIZARD_SIZE = 250
        WIZARD_SCALE = 3
        WIZARD_OFFSET = [112, 107]
        WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

        # load music and sounds
        pygame.mixer.music.load("assets/audio/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
        sword_fx.set_volume(0.5)
        magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
        magic_fx.set_volume(0.75)

        # load background image
        bg_image = pygame.image.load("assets/images/background/fon2.png").convert_alpha()

        start_im = pygame.image.load("assets/images/background/fon.jpg").convert_alpha()

        # load spritesheets
        warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
        wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

        # load vicory image
        victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

        game_over_img = pygame.image.load("GameOver.png").convert_alpha()

        # define number of steps in each animation
        WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
        WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

        FLAG = False

        # define font
        count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
        score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

        def start_screen():
            scaled_st = pygame.transform.scale(start_im, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_st, (0, 0))

        # function for drawing text
        def draw_text(text, font, text_col, x, y):
            img = font.render(text, True, text_col)
            screen.blit(img, (x, y))

        # function for drawing background
        def draw_bg():
            scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_bg, (0, 0))

        # function for drawing fighter health bars
        def draw_health_bar(health, x, y):
            ratio = health / 70
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(screen, RED, (x, y, 400, 30))
            pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

        # create two instances of fighters
        player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, 70)
        player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 70)

        # game loop
        run = True
        while run:

            clock.tick(FPS)

            start_screen()

            # draw background
            draw_bg()

            # show player stats
            draw_health_bar(player_1.health, 60, 20)
            draw_health_bar(player_2.health, 730, 20)
            draw_text("P1: " + str(score[0]), score_font, RED, 60, 60)
            draw_text("P2: " + str(score[1]), score_font, RED, 730, 60)

            # update countdown
            if intro_count <= 0:
                # move fighters
                player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2, round_over)
                player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1, round_over)
            else:
                # display count timer
                draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                # update count timer
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

            # update fighters
            player_1.update()
            player_2.update()

            # draw fighters
            player_1.draw(screen)
            player_2.draw(screen)

            # check for player defeat
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
                # display victory image
                screen.blit(victory_img, (500, 300))
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 3
                    player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,
                                      sword_fx, 70)
                    player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 70)

            if score[0] == 3 or score[1] == 3:
                screen.blit(game_over_img, (500, 300))
                round_over = True

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # update display
            pygame.display.update()

        # exit pygame
        pygame.quit()

    def slz_glav_window_opn(self):
        mixer.init()
        pygame.init()

        # create game window
        SCREEN_WIDTH = 1200
        SCREEN_HEIGHT = 700

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wild West")

        # set framerate
        clock = pygame.time.Clock()
        FPS = 60

        # define colours
        RED = (255, 15, 192)
        GREEN = (0, 255, 0)
        WHITE = (255, 255, 255)

        # define game variables
        intro_count = 3
        last_count_update = pygame.time.get_ticks()
        score = [0, 0]  # player scores. [P1, P2]
        round_over = False
        ROUND_OVER_COOLDOWN = 2000

        # define fighter variables
        WARRIOR_SIZE = 162
        WARRIOR_SCALE = 4
        WARRIOR_OFFSET = [72, 56]
        WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
        WIZARD_SIZE = 250
        WIZARD_SCALE = 3
        WIZARD_OFFSET = [112, 107]
        WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

        # load music and sounds
        pygame.mixer.music.load("assets/audio/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
        sword_fx.set_volume(0.5)
        magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
        magic_fx.set_volume(0.75)

        # load background image
        bg_image = pygame.image.load("assets/images/background/fon2.png").convert_alpha()

        start_im = pygame.image.load("assets/images/background/fon.jpg").convert_alpha()

        # load spritesheets
        warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
        wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

        # load vicory image
        victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

        game_over_img = pygame.image.load("GameOver.png").convert_alpha()

        # define number of steps in each animation
        WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
        WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

        FLAG = False

        # define font
        count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
        score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

        def start_screen():
            scaled_st = pygame.transform.scale(start_im, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_st, (0, 0))

        # function for drawing text
        def draw_text(text, font, text_col, x, y):
            img = font.render(text, True, text_col)
            screen.blit(img, (x, y))

        # function for drawing background
        def draw_bg():
            scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_bg, (0, 0))

        # function for drawing fighter health bars
        def draw_health_bar(health, x, y):
            ratio = health / 110
            pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(screen, RED, (x, y, 400, 30))
            pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

        # create two instances of fighters
        player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, 110)
        player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 110)

        # game loop
        run = True
        while run:

            clock.tick(FPS)

            start_screen()

            # draw background
            draw_bg()

            # show player stats
            draw_health_bar(player_1.health, 60, 20)
            draw_health_bar(player_2.health, 730, 20)
            draw_text("P1: " + str(score[0]), score_font, RED, 60, 60)
            draw_text("P2: " + str(score[1]), score_font, RED, 730, 60)

            # update countdown
            if intro_count <= 0:
                # move fighters
                player_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_2, round_over)
                player_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player_1, round_over)
            else:
                # display count timer
                draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                # update count timer
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

            # update fighters
            player_1.update()
            player_2.update()

            # draw fighters
            player_1.draw(screen)
            player_2.draw(screen)

            # check for player defeat
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
                # display victory image
                screen.blit(victory_img, (500, 300))
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 3
                    player_1 = Player(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,
                                      sword_fx, 110)
                    player_2 = Player(2, 850, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 110)

            if score[0] == 3 or score[1] == 3:
                screen.blit(game_over_img, (500, 300))
                round_over = True

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # update display
            pygame.display.update()

        # exit pygame
        pygame.quit()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    st = Home()
    st.show()
    sys.exit(app.exec())
