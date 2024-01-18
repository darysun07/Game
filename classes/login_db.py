# импорт библиотеки
import sqlite3


class LoginDb:
     # подключение базы данных
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # запросы в бд
    def is_table(self, table_name):
        query = "SELECT name from sqlite_master WHERE type='table' AND name='{}';".format(table_name)
        cursor = self.conn.execute(query)
        result = cursor.fetchone()
        if result is None:
            return False
        else:
            return True