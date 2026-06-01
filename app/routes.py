from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', title='MineCode - Главная')

@main.route('/fundamentals')
def fundamentals():
    return render_template('fundamentals.html', title='Теория команд Minecraft', body_class='basic-bg')
