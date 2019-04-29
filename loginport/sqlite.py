#coding=utf-8
import sqlite3

class Mydb:
    def __init__(self,dbname):#链接数据库
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def createtable(self,command):#创建表
        self.cursor.execute(command)

    def insertdt(self,command):
        self.cursor.execute(command)


db=Mydb("mydb.db")
