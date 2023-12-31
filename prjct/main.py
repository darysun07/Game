import sys
import pygame
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlTableModel

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

    def glav_window_opn(self):
        self.glav_window = Fon()
        self.glav_window.show()

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
            self.glav_window_opn()
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


pygame.init()


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
size = SCREEN_WIDTH, SCREEN_HEIGHT
screen = pygame.display.set_mode(size)
bg_im = pygame.image.load("fon2.png").convert_alpha()


def draw_bg():
  scaled_bg = pygame.transform.scale(bg_im, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.hero = pygame.image.load('hero.png').convert_alpha()
        self.hero.set_colorkey((255, 255, 255))
        self.rect_hero = self.hero.get_rect()
        self.rect_hero.x = x
        self.rect_hero.y = y

    def draw(self, surface):
        surface.blit(self.hero, (self.rect_hero.x, self.rect_hero.y))


running = True


vel = 5
jump = False
jumpCount = 0
jumpMax = 15
FPS = 60
clock = pygame.time.Clock()

hero1 = Hero(250, 250)

while running:
    draw_bg()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            if event.type == pygame.KEYDOWN:
                if not jump and event.key == pygame.K_SPACE:
                    jump = True
                    jumpCount = jumpMax
        keys = pygame.key.get_pressed()
        if jump:
            y_h -= jumpCount
            if jumpCount > -jumpMax:
                jumpCount -= 1
            else:
                jump = False
    hero1.update()
    hero1.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()


class Pravila(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pravila.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    st = Home()
    st.show()
    sys.exit(app.exec())