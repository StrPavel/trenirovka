import sqlite3
import math
import time


class Fdatabase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    #внесение в бд нового пользователя
    def addUser(self, name, email, hpsw, sex, age, targets, ves, trener):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count']>0:
                print("Пользователь с таким email уже существует")
                return False
            self.__cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, NULL)', (name, email, sex, age, targets, ves, trener, hpsw ))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД "+str(e))
            return False
        return True
    
    #авторизация
    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False 
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False
    
    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('Неверный логин')
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False
    
    #добавление аватара в бд
    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False
        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: "+str(e))
            return False
        return True
    
    #добавление тренировок в бд
    def addTren(self, tren, dates, id_users):
        try:
            self.__cur.execute('INSERT INTO tren VALUES(NULL, ?, ?, ?, 0 )', (tren, dates, id_users))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления "+str(e))
            return False
        return True
    
    #отображение из бд тренировок
    def getTrenAnonce(self, dates, id):
        try:
            self.__cur.execute(f"SELECT tren, id FROM tren WHERE dates = ? AND id_users = ? AND stat = ?", (dates, id, 0))
            res = self.__cur.fetchall()
            if res: 
                return res
        except sqlite3.Error as e:
            print("Ошибка  "+str(e))
        return ('Нет тренировок')
    
    #изменение в бд тренировка на выполнено(меняет статус с 0)
    def stat(self, id):
        try:
            self.__cur.execute("UPDATE tren SET stat = ? WHERE id = ?", (id, id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка  "+str(e))
            return False
        return True