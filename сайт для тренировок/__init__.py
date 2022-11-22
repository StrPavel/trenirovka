from flask import Flask, flash, render_template, url_for, request, g, flash,session, abort, redirect, make_response
from requests import session
from werkzeug.security import generate_password_hash, check_password_hash
from distutils.debug import DEBUG
from gc import get_debug
import sqlite3
import os
from Fdatabase import Fdatabase
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm, TrenForm, EndForm
import datetime


DATABASE = "/tmp/flsite.db"
DEBUG = True
SECRET_KEY = 'QWEER1323GS'


app = Flask(__name__)
app.config.from_object(__name__)

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = Fdatabase(db)


app.config.update(dict(DATABASE = os.path.join(app.root_path, "flsite.db")))
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Авторизуйтесь"
login_manager.login_message_category = "success"
MAX_CONTENT_LENGTH = 1024 * 1024
#создаю кнопки для меню майта
button = {'name' : "ДОБАВИТЬ ТРЕНИРОВКУ", 'url' : "/tren",'name1' : 'ПРОФИЛЬ', 'url1' : '/profile','name2' : 'ВЫЙТИ', 'url2' : '/logout'}

#создаю функции для создания БД, открытия и закрытия
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

#авторизация
@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)

#ввод логина и пароля
@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['psw'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.rember.data
            login_user(userlogin)
            return redirect(request.args.get('next') or url_for("profile"))
    return render_template("login.html",  form = form)

#регистрация
@app.route("/register", methods=["POST", "GET"])
def register():
   form = RegisterForm()
   if form.validate_on_submit():
        hash = generate_password_hash(request.form['psw'])
        res = dbase.addUser(form.name.data, form.email.data, hash, form.sex.data, form.age.data, form.targets.data, form.ves.data,form.trener.data )
        if res:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", "error")
 
   return render_template("register.html", form=form)
#главная страница на котоой отображается меню, и три даты(вчера сегодня, завтра) с тренировками
@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    img = current_user.getAvatar(app)
    monthRus = [0, 'января', "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентебря", "октября", "ноября", "декабря"]
    v = datetime.date.today() - datetime.timedelta(days=1)
    s = datetime.date.today()
    z = datetime.date.today() + datetime.timedelta(days=1)
    
    return render_template("profile.html",img = img, dt_now = [v.day,monthRus[v.month], s.day,monthRus[s.month], z.day, monthRus[z.month]], tren=[dbase.getTrenAnonce(v,current_user.get_id()),dbase.getTrenAnonce(s,current_user.get_id()),dbase.getTrenAnonce(z,current_user.get_id())], button = button)

#окно с тренироками на сегодня и ссылкой дляотметки что тренировка сделана
@app.route('/tooday', methods=['POST', 'GET'])
@login_required
def tooday():
    dt_now = datetime.date.today()
    form = EndForm()
    return render_template("tooday.html", dt_now = dt_now, tren=dbase.getTrenAnonce(dt_now,current_user.get_id() ), form = form,  button = button)

#окно с тренироками на вчера и ссылкой дляотметки что тренировка сделана
@app.route('/vhera', methods=['POST', 'GET'])
@login_required
def vhera():
    dt_now = datetime.date.today() - datetime.timedelta(days=1)
    form = EndForm()
    return render_template("vhera.html", dt_now = dt_now, tren=dbase.getTrenAnonce(dt_now,current_user.get_id() ), form = form, button = button)

#окно с тренироками на завтра и ссылкой дляотметки что тренировка сделана
@app.route('/yestoday', methods=['POST', 'GET'])
@login_required
def yestoday():
    dt_now = datetime.date.today() + datetime.timedelta(days=1)
    form = EndForm()
    return render_template("yestoday.html", dt_now = dt_now, tren=dbase.getTrenAnonce(dt_now,current_user.get_id() ), form = form,  button = button)

#добавления тренировок, 
@app.route('/tren',  methods=['POST', 'GET'])
@login_required
def tren():
    form = TrenForm()
    if form.validate_on_submit():
        if form.id_pol.data:
            res = dbase.addTren(form.tren.data, form.dates.data, form.id_pol.data )
        else:
            res = dbase.addTren(form.tren.data, form.dates.data, current_user.get_id() )
        if res:
            flash("Добавлено", "success")
            return redirect(url_for('login'))
        else:
            flash("Ошибка", "error")
    return render_template("tren.html", form=form, button = button) 

#выход из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/')
def index():
    return redirect(url_for('login'))

#ссылка для завершение тренировка
@app.route("/<int:id>")
def showPost(id):
    dbase.stat(id)
    return redirect(url_for('profile'))

#окно для изменения профиля
@app.route('/zamena', methods=['POST', 'GET'])
@login_required
def zamena():
    return render_template("zamena.html", button = button)

#изменение авы
@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h

#обнавления аватара
@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash("Ошибка обновления аватара", "error")
                    return redirect(url_for('zamena'))
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", "error")
 
    return redirect(url_for('zamena'))


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)