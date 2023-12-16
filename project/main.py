import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlTableModel

import sqlite3
from add_trnsctn import Ui_Dialog
from trnsctndb_create import Dbbb


class LoginDb():
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
        uic.loadUi('homee.ui', self)

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

    def glav_window_opn(self):
        self.glav_window = Glav()
        self.glav_window.show()

    def signup_window_opn(self):
        self.signup_window_opn = Signup()
        self.signup_window_opn.show()
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
        uic.loadUi('log.ui', self)
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
        self.conn = Dbbb()
        self.view_data()
        self.reload_data()

        self.btn_add_trnsctn.clicked.connect(self.open_trnsctn_window)
        self.btn_remove_trnsctn.clicked.connect(self.delete_trnsctn)

    def reload_data(self):
        self.balance_all.setText(self.conn.all_blnc())
        self.up_blnc.setText(self.conn.all_up())
        self.down_blnc.setText(self.conn.all_down())
        self.credit_expense.setText(self.conn.all_crdt())
        self.grsries_clothes_blnc.setText(self.conn.all_products())
        self.transport_blnc.setText(self.conn.all_trnsprt())
        self.other_blnc.setText(self.conn.all_other())

    def view_data(self):
        self.model = QSqlTableModel(self)
        self.model.setTable('EXPENSES')
        self.model.select()
        self.tableView.setModel(self.model)

    def open_trnsctn_window(self):
        self.nwindow = QtWidgets.QDialog()
        self.ui_window = Ui_Dialog()
        self.ui_window.setupUi(self.nwindow)
        self.nwindow.show()
        self.ui_window.btn_save_trnsctn.clicked.connect(self.addd_trnsctn)

    def addd_trnsctn(self):
        date = self.ui_window.de_date.text()
        ctgry = self.ui_window.cbox_select_ctgry.currentText()
        dscrptn = self.ui_window.le_dscribe.text()
        blnce = self.ui_window.le_blnce.text()
        status = self.ui_window.select_up_or_down.currentText()

        self.conn.add_trnsctn(date, ctgry, dscrptn, blnce, status)
        self.view_data()
        self.reload_data()
        self.nwindow.close()

    def delete_trnsctn(self):
        index = self.tableView.selectedIndexes()[0]
        id = str(self.tableView.model().data(index))

        self.conn.del_trnsctn(id)
        self.view_data()
        self.reload_data()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    st = Home()
    st.show()
    sys.exit(app.exec())