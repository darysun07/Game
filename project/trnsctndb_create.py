import sys
from PyQt5 import QtSql
from PyQt5.QtCore import *
import sqlite3


class Dbbb:
    def __init__(self):
        super(Dbbb, self).__init__()
        self.cnctn()

    def cnctn(self):
        trnsctndb = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        trnsctndb.setDatabaseName('trnsctn.db')
        self.conn = sqlite3.connect('trnsctn.db')
        self.conn.execute("CREATE TABLE IF NOT EXISTS EXPENSES (ID INTEGER PRIMARY KEY AUTOINCREMENT, Date TEXT NOT NULL, "
                 "Category TEXT NOT NULL, Description TEXT NOT NULL, Balance REAL, Status TEXT NOT NULL)")
        self.conn.commit()
        return True
    
    def qry_with_prmtrs(self, sql_qry, values=None):
        qry = QtSql.QSqlQuery()
        qry.prepare(sql_qry)

        if values is not None:
            for value in values:
                qry.addBindValue(value)

        qry.exec()
        return qry

    def add_trnsctn(self, date, ctgry, dscrptn, balance, status):
        sql_query = "INSERT INTO EXPENSES (Date, Category, Description, Balance, Status) VALUES (?, ?, ?, ?, ?)"
        self.qry_with_prmtrs(sql_query, [date, ctgry, dscrptn, balance, status])

    def del_trnsctn(self, id):
        sql_query = 'DELETE FROM EXPENSES WHERE ID=?'
        self.qry_with_prmtrs(sql_query, [id])

    def get_blnc(self, column, filter=None, value=None):
        sql_query = f"SELECT SUM ({column}) FROM EXPENSES"

        if filter is not None and value is not None:
            sql_query += f" WHERE {filter} = ?"

        values = []
        if value is not None:
            values.append(value)

        qry = self.qry_with_prmtrs(sql_query, values)

        if qry.next():
            return str(qry.value(0)) + ' руб.'
        
        return '0'
    
    def all_blnc(self):
        return self.get_blnc(column='Balance')
    
    def all_up(self):
        return self.get_blnc(column='Balance', filter='Status', value='Доход')
    
    def all_down(self):
        return self.get_blnc(column='Balance', filter='Status', value='Расход(затраты)')
    
    def all_crdt(self):
        return self.get_blnc(column='Balance', filter='Category', value='Кредиты, налоги')
    
    def all_products(self):
        return self.get_blnc(column='Balance', filter='Category', value='Продукты питания, промтовары, одежда')
    
    def all_trnsprt(self):
        return self.get_blnc(column='Balance', filter='Category', value='Транспорт')
    
    def all_other(self):
        return self.get_blnc(column='Balance', filter='Category', value='Другое(досуг и т.д.)')