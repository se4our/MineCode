from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm

main = Blueprint('main', __name__)


# ========== ГЛАВНАЯ ==========
@main.route('/')
def index():
    return render_template('index.html', title='MineCode - Главная')


# ========== ТЕОРИЯ (статическая) ==========
@main.route('/fundamentals')
def fundamentals():
    return render_template('fundamentals.html', title='Теория команд Minecraft', body_class='basic-bg')


# ========== РЕГИСТРАЦИЯ ==========
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Регистрация успешна! Теперь войдите.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form, title='Регистрация')


# ========== ВХОД ==========
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data if hasattr(form, 'remember_me') else False)
            flash(f'Добро пожаловать, {user.username}!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.profile'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')

    return render_template('login.html', form=form, title='Вход')


# ========== ОБЩАЯ СТРАНИЦА (auth.html) ==========
@main.route('/auth')
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    reg_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('auth.html', title='Вход / Регистрация', body_class='theory-bg',
                           reg_form=reg_form, login_form=login_form)


@main.route('/register-ajax', methods=['POST'])
def register_ajax():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('main.profile'))

    login_form = LoginForm()
    return render_template('auth.html', title='Вход / Регистрация', body_class='theory-bg',
                           reg_form=form, login_form=login_form)


@main.route('/login-ajax', methods=['POST'])
def login_ajax():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data if hasattr(form, 'remember_me') else False)
            flash(f'Добро пожаловать, {user.username}!', 'success')
            return redirect(url_for('main.profile'))
        flash('Неверный логин или пароль', 'error')

    reg_form = RegistrationForm()
    return render_template('auth.html', title='Вход / Регистрация', body_class='theory-bg',
                           reg_form=reg_form, login_form=form)


# ========== ПРОФИЛЬ ==========
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Мой профиль')


# ========== ВЫХОД ==========
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'info')
    return redirect(url_for('main.index'))


# ========== ОШИБКИ ==========
@main.errorhandler(404)
def not_found(e):
    return render_template('error.html', title='Страница не найдена', code=404, message='Страница не найдена'), 404