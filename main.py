import os
from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data.news import News
from data.users import User
from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm
from forms.gallery import GalleryForm
from data.__all_models import users, news
from data import db_session, news_api

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(news_api.blueprint)
    app.run()


@app.route("/")
def index():
    formid = request.args.get('formid')
    category = [("ВОРОТА", "gates", os.listdir('static/img/gates'), len(os.listdir('static/img/gates'))),
                ("РЕШЕТКИ", "gratings", os.listdir('static/img/gratings'), len(os.listdir('static/img/gratings')))]
    if request.method == 'POST':
        f = request.files['file']
        catalog = request.form["hid"]
        print(catalog)
        pics = os.listdir(f'static/img/{catalog}')
        print(len(pics))
        with open(f'static/img/{catalog}/{len(pics) + 1}.jpg', 'wb') as file:
            file.write(f.read())
    return render_template("index.html", category=category)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
