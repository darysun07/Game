from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

import classes.signup
from classes.yrovni import Yrovni
from classes.pravila import Pravila
from classes.login_db import LoginDb


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/wild_west.ui', self)

        self.loginDb = LoginDb('assets/login.db')
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

    def signup_window_opn(self):
        self.signup_window_opn = classes.signup.Signup()
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