# импорт нужных библиотек и методов
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

# импорт нужных классов
import classes.home
from classes.login_db import LoginDb


class Signup(QMainWindow):
    def __init__(self):
        super().__init__()
        # подгрузка ui-файла
        uic.loadUi('ui/login.ui', self)
        # активация кнопки на окне
        self.reg_btn.clicked.connect(self.insertData)

        self.loginDb = LoginDb('assets/login.db')

    # регистрация нового пользователя
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
            self.home_window_opn = classes.home.Home()
            self.home_window_opn.show()
            self.close()