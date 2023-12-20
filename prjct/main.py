import sys
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
        self.glav_window = Glav()
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


class Glav(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('glav.ui', self)


class Pravila(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pravila.ui', self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    st = Home()
    st.show()
    sys.exit(app.exec())