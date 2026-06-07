from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, TestResult, TheorySection, Question
from app import db
from app.forms import RegistrationForm, LoginForm, TheorySectionForm, QuestionForm
from functools import wraps

main = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Доступ запрещён', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# Главная
@main.route('/')
def index():
    return render_template('index.html', title='MineCode - Главная')

# Теория (динамическая)
@main.route('/fundamentals')
def fundamentals():
    sections = TheorySection.query.order_by(TheorySection.order).all()
    return render_template('fundamentals.html', title='Теория команд Minecraft', body_class='theory-bg', sections=sections)

# Справочник команд
@main.route('/theory')
def theory():
    return render_template('theory.html', title='Справочник команд', body_class='theory-bg')

# Практика (тесты)
@main.route('/practice')
def practice():
    return render_template('practice.html', title='Практические тесты', body_class='theory-bg')

# Страница теста
@main.route('/test')
def test():
    topic = request.args.get('topic', 'Неизвестная тема')
    difficulty = request.args.get('difficulty', 'easy')
    return render_template('test.html', title=f'Тест: {topic}', topic=topic, difficulty=difficulty, body_class='theory-bg')

# Регистрация / вход
@main.route('/auth')
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    reg_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('auth.html', title='Вход / Регистрация', body_class='theory-bg', reg_form=reg_form, login_form=login_form)

@main.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('main.index'))
    login_form = LoginForm()
    return render_template('auth.html', title='Вход / Регистрация', body_class='theory-bg', reg_form=form, login_form=login_form)

@main.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вход выполнен', 'success')
            return redirect(url_for('main.index'))
        flash('Неверный логин или пароль', 'error')
    reg_form = RegistrationForm()
    return render_template('auth.html', title='Вход / Регистрация', body_class='theory-bg', reg_form=reg_form, login_form=form)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Профиль', body_class='theory-bg')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('main.index'))

# CRUD для теории (только admin)
@main.route('/fundamentals/manage')
@admin_required
def manage_theory():
    sections = TheorySection.query.order_by(TheorySection.order).all()
    return render_template('manage_theory.html', title='Управление теорией', body_class='theory-bg', sections=sections)

@main.route('/fundamentals/create', methods=['GET', 'POST'])
@admin_required
def create_theory():
    form = TheorySectionForm()
    if form.validate_on_submit():
        section = TheorySection(title=form.title.data, content=form.content.data, order=form.order.data)
        db.session.add(section)
        db.session.commit()
        flash('Раздел создан', 'success')
        return redirect(url_for('main.manage_theory'))
    return render_template('edit_theory.html', title='Новый раздел', body_class='theory-bg', form=form)

@main.route('/fundamentals/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_theory(id):
    section = TheorySection.query.get_or_404(id)
    form = TheorySectionForm(obj=section)
    if form.validate_on_submit():
        section.title = form.title.data
        section.content = form.content.data
        section.order = form.order.data
        db.session.commit()
        flash('Раздел обновлён', 'success')
        return redirect(url_for('main.manage_theory'))
    return render_template('edit_theory.html', title='Редактировать раздел', body_class='theory-bg', form=form)

@main.route('/fundamentals/delete/<int:id>', methods=['POST'])
@admin_required
def delete_theory(id):
    section = TheorySection.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    flash('Раздел удалён', 'success')
    return redirect(url_for('main.manage_theory'))

# Управление вопросами тестов (только админ)
@main.route('/practice/manage')
@admin_required
def manage_practice():
    return render_template('manage_practice.html', title='Управление вопросами', body_class='theory-bg')

@main.route('/practice/create', methods=['GET', 'POST'])
@admin_required
def create_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(
            topic=form.topic.data,
            difficulty=form.difficulty.data,
            type=form.type.data,
            question_text=form.question_text.data,
            options=form.options.data,
            correct_answer=form.correct_answer.data,
            explanation=form.explanation.data,
            order=form.order.data
        )
        db.session.add(question)
        db.session.commit()
        flash('Вопрос создан', 'success')
        return redirect(url_for('main.manage_practice'))
    return render_template('edit_question.html', title='Новый вопрос', body_class='theory-bg', form=form)

@main.route('/practice/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_question(id):
    question = Question.query.get_or_404(id)
    form = QuestionForm(obj=question)
    if form.validate_on_submit():
        form.populate_obj(question)
        db.session.commit()
        flash('Вопрос обновлён', 'success')
        return redirect(url_for('main.manage_practice'))
    return render_template('edit_question.html', title='Редактировать вопрос', body_class='theory-bg', form=form)

@main.route('/practice/delete/<int:id>', methods=['POST'])
@admin_required
def delete_question(id):
    question = Question.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    flash('Вопрос удалён', 'success')
    return redirect(url_for('main.manage_practice'))

@main.route('/api/questions')
def api_questions():
    topic = request.args.get('topic')
    difficulty = request.args.get('difficulty')
    questions = Question.query.filter_by(topic=topic, difficulty=difficulty).order_by(Question.order).all()
    if not questions:
        return jsonify([])
    result = []
    for q in questions:
        item = {
            'type': q.type,
            'question': q.question_text,
            'options': q.options.split('\n') if q.options else [],
            'correct': int(q.correct_answer) if q.type == 'theory' else q.correct_answer,
            'explanation': q.explanation or ''
        }
        result.append(item)
    return jsonify(result)

@main.route('/api/topics_by_difficulty')
@admin_required
def api_topics_by_difficulty():
    difficulty = request.args.get('difficulty')
    if not difficulty:
        return jsonify([])
    topics = db.session.query(Question.topic).filter_by(difficulty=difficulty).distinct().all()
    return jsonify([t[0] for t in topics])

@main.route('/api/manage/questions')
@admin_required
def api_manage_questions():
    topic = request.args.get('topic')
    difficulty = request.args.get('difficulty')
    if not topic or not difficulty:
        return jsonify([])
    questions = Question.query.filter_by(topic=topic, difficulty=difficulty).order_by(Question.order).all()
    result = []
    for q in questions:
        result.append({
            'id': q.id,
            'type': q.type,
            'question_text': q.question_text,
            'options': q.options,
            'correct_answer': q.correct_answer,
            'explanation': q.explanation,
            'order': q.order
        })
    return jsonify(result)

# API эндпоинт рейтинга (заглушка)
@main.route('/api/rating')
def api_rating():
    data = [
        {"place": 1, "player": "Steve", "score": 42.5},
        {"place": 2, "player": "Alex", "score": 38.0},
        {"place": 3, "player": "Notch", "score": 35.5},
    ]
    return jsonify(data)

# Страницы ошибок
@main.errorhandler(404)
def not_found(e):
    return render_template('error.html', title='Страница не найдена', code=404, message='Страница не найдена'), 404

@main.errorhandler(500)
def server_error(e):
    return render_template('error.html', title='Ошибка сервера', code=500, message='Внутренняя ошибка сервера'), 500