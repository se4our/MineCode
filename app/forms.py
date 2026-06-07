from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя уже занято.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже используется.')

class LoginForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class TheorySectionForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    order = IntegerField('Порядок', default=0)
    submit = SubmitField('Сохранить')

class QuestionForm(FlaskForm):
    topic = StringField('Тема', validators=[DataRequired(), Length(max=100)])
    difficulty = SelectField('Сложность', choices=[('easy', 'Лёгкая'), ('medium', 'Средняя'), ('hard', 'Сложная')], validators=[DataRequired()])
    type = SelectField('Тип вопроса', choices=[('theory', 'Теоретический'), ('practice', 'Практический')], validators=[DataRequired()])
    question_text = TextAreaField('Текст вопроса', validators=[DataRequired()])
    options = TextAreaField('Варианты ответов (для теории: по одному на строку, правильный отметьте звёздочкой *)')
    correct_answer = StringField('Правильный ответ (для практики: строка или несколько вариантов через запятую)', validators=[DataRequired()])
    explanation = TextAreaField('Пояснение')
    order = IntegerField('Порядок', default=0)
    submit = SubmitField('Сохранить')