from flask import render_template, abort, jsonify, g, request
from flask_login import current_user
from flask_httpauth import HTTPBasicAuth

import datetime

from app.models import User, Item, Association
from app import app, db

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.check_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True


#########
#  API  #
#########

# TODO: Remove?
# @app.route('/api/v1/login', methods=['POST'])
# def api_login():
#     data = request.json
#     if not data:
#         abort(400)
#     user = User.query.filter_by(username=data['username']).first()
#     if user is None or not user.check_password(data['password']):
#         return jsonify({'error': 'wrong username or/and password'}), 400
#
#     login_user(user)
#
#     return jsonify(message='successful login', token=user.get_token()), 200

@app.route('/api/v1/register', methods=['POST'])
def api_register():
    """
    `username, password, birth_date, register_date, email, phone_number`
    :return:
    """
    def exists_(username, email):
        username_query = User.query.filter_by(username=username).first()
        email_query = User.query.filter_by(email=email).first()
        if username_query is None and email_query is None:
            return False
        return True

    data = request.json

    if not data:
        abort(400)
    for p in ['username', 'password', 'register_date', 'email', 'phone_number', 'birth_date']:
        if (p not in data) or type(data[p]) != str:
            abort(400)

    if exists_(data['username'], data['email']):
        return jsonify({'error': 'user already exist'}), 400

    cur_user = User(
        username=data['username'],
        birth_date=data['birth_date'],
        register_date=data['register_date'],
        email=data['email'],
        phone_number=data['phone_number']
    )
    cur_user.set_password(data['password'])
    db.session.add(cur_user)
    db.session.commit()
    return jsonify(message='user added successfully'), 200


@app.route('/api/v1/token')
@auth.login_required
def get_auth_token():
    token = g.user.get_token()
    return jsonify({'token': token})


@app.route('/api/v1/new_item', methods=['POST'])
@auth.login_required
def api_new_item():
    """
    Create new item in the store.
    :return:
    """
    req_json = request.json

    if not req_json:
        abort(400)

    if ('title' not in req_json) or type(req_json['title']) != str:
        abort(400)
    if ('category' not in req_json) or type(req_json['category']) != str:
        abort(400)

    item = Item(title=req_json['title'],
                description=req_json.get('description', ""),
                date_added=today(),
                category=req_json['category'])

    db.session.add(item)
    db.session.commit()

    return jsonify(task=get_item_json(item)), 201


def today():
    return str(datetime.datetime.now().date())


def get_item_json(item):
    return {'id': item.id,
            'title': item.title,
            'description': item.description,
            'date_added': item.date_added,
            'category': item.category}


@app.route('/api/v1/update_item/<int:item_id>', methods=['PUT'])
@auth.login_required
def api_update_item(item_id):
    """
    Update parameters of the stored item.
    :param item_id:
    :return:
    """
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
        abort(400)

    req_json = request.json
    if not req_json:
        abort(400)
    if 'title' in req_json and type(req_json['title']) != str:
        abort(400)
    if 'description' in req_json and type(req_json['description']) != str:
        abort(400)

    item.title = req_json.get('title', item.title)
    item.description = req_json.get('description', item.description)

    db.session.add(item)
    db.session.commit()

    return jsonify(task=get_item_json(item))


@app.route('/api/v1/all_items', methods=['GET'])
@auth.login_required
def api_all_items():
    """
    List all items in the store.
    :return:
    """
    items = [get_item_json(item) for item in Item.query.all()]
    res = jsonify(items=items)
    return res


@app.route('/api/v1/get_item/<int:item_id>', methods=['GET'])
@auth.login_required
def api_get_item(item_id):
    """
    Returns information related to item with id `item_id`.
    :param item_id:
    :return:
    """
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
        abort(400)
    return jsonify(get_item_json(item))


@app.route('/api/v1/add_cart', methods=['POST'])
@auth.login_required
def api_add_cart():
    """
    Add item to cart.
    :return:
    """
    req_json = request.json
    if not req_json:
        abort(400)

    for p in ['user_id', 'item_id', 'amount']:
        if p not in req_json:
            abort(400)

    item = Item.query.filter_by(id=req_json['item_id']).first()
    if item is None:
        abort(400)

    user = User.query.filter_by(id=req_json['user_id']).first()
    if user is None:
        abort(400)

    idx = get_index_of_item(user, item.id)
    amount = int(req_json['amount'])
    print(idx)
    if idx == -1:
        a = Association(amount=amount)
        a.item = item
        user.cart.append(a)
    else:
        user.cart[idx].amount += amount

    db.session.add(user)
    db.session.commit()

    record = {
        'user_id': req_json['user_id'],
        'item_id': req_json['item_id'],
        'amount': req_json['amount']
    }
    return jsonify(record=record), 201


def get_index_of_item(user, item_id):
    cart = user.cart
    for i in range(len(cart)):
        if cart[i].item.id == item_id:
            return i
    return -1


@app.route('/api/v1/cart/<int:user_id>', methods=['GET'])
@auth.login_required
def api_cart(user_id):
    """
    List all items in the cart of user with id `user_id`.
    :return:
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    cart = [{'item': get_item_json(item.item), 'amount': item.amount} for item in user.cart]

    res = jsonify(cart=cart)
    return res


#####################
#  Other Endpoints  #
#####################

@app.route('/')
@app.route('/index')
def index():

    username = current_user.username

    # if is_admin:
    #     actions = [
    #         {
    #             'title': "new_item",
    #             'text': 'Добавить новый товар в ассортимент'
    #         }
    #     ]
    # else:
    #     actions = [
    #         {
    #             'title': "view_cart",
    #             'text': 'Просмотр корзины'
    #         },
    #         {
    #             'title': "add_cart",
    #             'text': 'Добавить товар в корзину'
    #         }
    #     ]
    # return render_template('index.html', title='Дашборд', user=username, actions=actions)
    return render_template('index.html', title='Дашборд', user=username)


# @app.route('/new_item')
# def new_item():
#     return render_template('new_item.html', title='Добавление нового товара', user=user)
#
#
# @app.route('/add_cart')
# def add_cart():
#     return render_template('add_cart.html', title='Добавить товар в корзину', user=user)
#
#
# @app.route('/view_cart')
# def view_cart():
#     return render_template('view_cart.html', title='Корзина', user=user)
