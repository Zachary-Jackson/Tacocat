from flask import (Flask, render_template, flash, redirect, url_for, g)
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user, login_required,
                         current_user)


import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'exta.secret.keyoisdfjjj938rijs&*&*'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    """This finds a user or return None"""
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each requrest."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Closes the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
def index():
    """This is Tacocat's main homepage."""
    tacos = models.Taco.select().limit(100)
    return render_template('index.html', tacos=tacos)


@app.route('/register', methods=('GET', 'POST'))
def register():
    """This is the new user registration page."""
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You are registered!", "success")
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    """This page allows the user to login."""
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email does not exist :{")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Welcome to Tacocat!", "success")
                return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """This page allows the user to logout."""
    logout_user()
    flash("Leaving is only premissable if you are going to make new tacos.")
    return redirect(url_for('index'))


@app.route('/post', methods=('GET', 'POST'))
@login_required
def post():
    """This lets a user submit a post."""
    form = forms.TacoForm()
    if form.validate_on_submit():
        models.Taco.create(user=g.user.id,
                           protein=form.protein.data.strip().lower(),
                           shell=form.shell.data.strip().lower(),
                           cheese=form.cheese.data.strip().lower(),
                           extras=form.extras.data.strip().lower())
        return redirect(url_for('index'))
    return render_template("taco.html", form=form)


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            email="example@example.com",
            password="password",
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
