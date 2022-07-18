from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    mock_posts = [
        {
            'author': {'username': 'micheal'},
            'body': 'micheals blog post'
        },
        {
            'author': {'username': 'the_other_micheal'},
            'body': "this isn't micheals blog post"
        }
    ]
    return render_template('index.html', title="Home", posts=mock_posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()

        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username / password')
            return redirect(url_for("login"))

        login_user(user, remember=login_form.remember_me.data)

        stored_page = request.args.get('next')
        if not stored_page or url_parse(stored_page).netloc != '':
            stored_page = url_for("index")

        return redirect(url_for(stored_page))

    return render_template('login.html', title='Sign In', form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        user = User(username=registration_form.username.data, email=registration_form.email.data)
        user.set_password(registration_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=registration_form)
