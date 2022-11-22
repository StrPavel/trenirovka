from flask_login import LoginManager
from flask import Flask, flash, render_template, url_for, request, g, flash,session, abort, redirect

#добавление данных о пользователя в сессию
class UserLogin:
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self
 
    def create(self, user):
        self.__user = user
        return self
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return str(self.__user['id'])

    def getName(self):
        return self.__user['name'] if self.__user else "без имени"
    
    
    def getEmail(self):
        return self.__user['Email'] if self.__user else "без Email"

    def getSex(self):
        return self.__user['sex'] if self.__user else "неизвестно"

    def getAge(self):
        return self.__user['age'] if self.__user else "неизвестно"
    
    def getVes(self):
        return self.__user['ves'] if self.__user else "неизвестно"

    def getTrener(self):
        return self.__user['trener'] if self.__user else "без Тренера"
    
    def getTargets(self):
        return self.__user['targets'] if self.__user else "без Цели"

    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='/foto/default.jpg'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: "+str(e))
        else:
            img = self.__user['avatar']
 
        return img

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == "JPG" or ext == "jpg":
            return True
        return False