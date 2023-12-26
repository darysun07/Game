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


class Fon(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.image.load('ground.png').convert_alpha()
        self.fon = pygame.image.load('fon2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 535
        self.fon_coord = self.fon.get_rect()
        self.fon_coord.x = 0
        self.fon_coord.y = 0
        #screen.blit(self.fon, (self.fon_coord.x, self.fon_coord.y))
        #screen.blit(self.image, (self.rect.x, self.rect.y))


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.hero = pygame.image.load('hero.png').convert()
        self.rect_hero = self.hero.get_rect()
        self.rect_hero.x = 0
        self.rect_hero.y = 150


pygame.init()
size = width, height = 1200, 700
screen = pygame.display.set_mode(size)
running = True

fon = Fon()
hero = Hero(50, 50)
hero_f_sprites = pygame.sprite.Group()
hero_f_sprites.add(fon, hero)
image = pygame.image.load('ground.png').convert_alpha()
screen.blit(image, (width, height))
vel = 5
jump = False
jumpCount = 0
jumpMax = 15
FPS = 60
clock = pygame.time.Clock()
while running:
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
    #rect.topleft = (x, y)
    hero_f_sprites.update()
    hero_f_sprites.draw(screen)
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