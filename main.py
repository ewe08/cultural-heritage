from flask import render_template, redirect, request
from flask import Flask
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os

from data import db_session
from data.products import Object
from data.comments import Comment
from data.users import User
from forms.comment import CommentForm
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.products import ObjectForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = r'static\img'
login_manager = LoginManager()
login_manager.init_app(app)


# 772c6ef89b0ef87bededd6647107b4fd1b2586b157e0540405e917a789c5d581 - api_key


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/info')
@login_required
def info():
    db_sess = db_session.create_session()
    all_user_products = db_sess.query(Object)
    return render_template("info.html", user=current_user, prods=all_user_products)


@app.route("/objects")
def objects():
    db_sess = db_session.create_session()
    prods = db_sess.query(Object).all()
    return render_template("objects.html", prods=prods)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/objects")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addobj', methods=['GET', 'POST'])
@login_required
def add_obj():
    try:
        form = ObjectForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            obj = Object(
                object=form.name.data,
                place=form.place.data,
                category=form.category.data,
                type=form.type.data,
                in_UNESCO=form.in_UNESCO.data
            )
            img = form.picture.data
            obj = str(db_sess.query(obj)[-1].id)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{obj}.png'))
            return redirect('/objects.html')
        return render_template('products.html', title='Добавить объект',
                               form=form)
    except Exception:
        return render_template('products.html', message="Данные введены неверно", form=form)


@app.route('/object/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_prod(id):
    if current_user.admin_status == 1:
        form = ObjectForm()
        if request.method == "GET":
            db_sess = db_session.create_session()
            prod = db_sess.query(Object).filter(Object.id == id).first()

            if prod:
                form.name.data = prod.name
                form.place.data = prod.address_text
                form.category.data = prod.category
                form.type.data = prod.object_type
                form.info.data = prod.info
                form.in_UNESCO.data = prod.unesco_status
                form.picture.data = prod.photo

            else:
                abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            prod = db_sess.query(Object).filter(Object.id == id).first()

            if prod:
                prod.name = form.name.data
                prod.address_text = form.place.data
                prod.category = form.category.data
                prod.object_type = form.type.data
                prod.info = form.info.data

                if form.in_UNESCO.data:
                    prod.unesco_status = 1
                else:
                    prod.unesco_status = 0

                prod.photo = form.picture.data
                db_sess.commit()
                return redirect('/objects')
            else:
                abort(404)
        return render_template('products.html',
                               title='Редактирование задания',
                               form=form, prod=prod
                               )
    else:
        return "<h1>Отказано в доступе</h1>"


@app.route('/object_info/<int:id>', methods=['GET', 'POST'])
def object_info(id):
    db_sess = db_session.create_session()
    prod = db_sess.query(Object).filter(Object.id == id).first()
    comms = db_sess.query(Comment).filter(Comment.post == id)
    if prod:
        return render_template("object_info.html", prods=prod, comm=comms)
    else:
        abort(404)
    return redirect('/objects')

@app.route('/obj_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def prod_delete(id):
    if current_user.admin_status == 1:
        db_sess = db_session.create_session()
        prod = db_sess.query(Object).filter(Object.id == id).first()
        if prod:
            db_sess.delete(prod)
            db_sess.commit()
        else:
            abort(404)
        return redirect('/shop')
    else:
        return "<h1>Отказано в доступе</h1>"

@app.route('/object_comments/<int:id>', methods=['GET', 'POST'])
def object_comments(id):
    form = CommentForm()
    try:
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            com = Comment(
                user=current_user.id,
                post=id,
                text=form.comment.data
            )
            com = str(db_sess.query(com)[-1].id)
            return redirect('/objects.html')
        return render_template('object_comments.html', title='Добавить комментарий',
                               form=form)
    except Exception:
        return render_template('object_comments.html', message="Данные введены неверно", form=form)


if __name__ == '__main__':
    db_sess = db_session.global_init(f"db/Culture.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
