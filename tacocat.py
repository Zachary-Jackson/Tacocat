from flask import (Flask, render_template, flash, redirect, url_for)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user, login_required)


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
    except models.DoesNotExsist:
        return None


@app.route('/')
def index():
    """This is Tacocat's main homepage."""
    return render_template('layout.html')


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
            flash("Your email does not exsist :{")
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
