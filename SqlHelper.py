# coding=utf8

import os
import sqlite3
import config


def SafeInput(val):
    return val.replace('\'', '＇')


class Sqlite:
    def __init__(self):
        self.dbPath = os.path.join(os.getcwd(), config.sqliteDbPath)

    def __GetConnect(self):
        if not self.dbPath:
            raise (NameError, "not set dbpath")
        self.conn = sqlite3.connect(self.dbPath)

        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "connect db fail")
        return cur
        
    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    sqt = Sqlite(os.path.join(os.getcwd(), 'test.db'))
    cateList = sqt.ExecQuery("SELECT * FROM cate WHERE layer=1")
    for cate in cateList:
        print(cate)

