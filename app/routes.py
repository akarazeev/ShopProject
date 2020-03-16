from flask import render_template
from app import app

user = {'username': 'test'}
# user = {'username': 'admin'}

# is_admin = False
is_admin = user['username'] == 'admin'

@app.route('/')
@app.route('/index')
def index():
    if is_admin:
        actions = [
            {
                'title': "new_item",
                'text': 'Добавить новый товар в ассортимент'
            }
        ]
    else:
        actions = [
            {
                'title': "view_cart",
                'text': 'Просмотр корзины'
            },
            {
                'title': "add_cart",
                'text': 'Добавить товар в корзину'
            }
        ]

    return render_template('index.html', title='Дашборд', user=user, actions=actions)


@app.route('/new_item')
def new_item():
    return render_template('new_item.html', title='Добавление нового товара', user=user)


@app.route('/add_cart')
def add_cart():
    return render_template('add_cart.html', title='Добавить товар в корзину', user=user)


@app.route('/view_cart')
def view_cart():
    return render_template('view_cart.html', title='Корзина', user=user)
