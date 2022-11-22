from email import message
from email.policy import default
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Email, Length, EqualTo

#формы для логина и пароля
class LoginForm(FlaskForm):
    email = StringField("Email: ", validators = [Email('Некоректный Email')])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])
    rember = BooleanField('Запомнить', default = False)
    submit = SubmitField('Войти')


#формы для регистрации
class RegisterForm(FlaskForm):
    name = StringField("Имя: ", validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")])
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    sex = StringField("Пол: ")
    age = StringField("Возвраст: ")
    targets = StringField("Цель: ", validators=[Length(min=4, max=100, message="Должно быть от 4 до 100 символов")])
    ves = StringField("Вес: ")
    trener = StringField("id тренера(если есть): ")
    psw = PasswordField("Пароль: ", validators = [DataRequired(), Length(min = 4, max = 100, message="Пароль должен быть от 4 до 100 символов")])
    psw2 = PasswordField("Повторите пароль: ", validators=[DataRequired(), EqualTo("psw", message="Пароли не совпадают")])
    submit = SubmitField("Регистрация")


#формы для добавления тренировок
class TrenForm(FlaskForm):
    tren = TextAreaField('ТРЕНИРОВКА: ')
    dates = DateField("ДАТА: ")
    id_pol = StringField("Введите id пользователя: ")
    submit = SubmitField("Добавить: ")


#форма для изменения профиля
class EndForm(FlaskForm):
    submit = SubmitField("Профиль")
