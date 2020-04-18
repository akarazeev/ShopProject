import datetime

from flask import render_template, abort, jsonify, g, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Item, Association
from app import app, db

user = {'username': 'test'}
# user = {'username': 'admin'}

db_items = list()
db_cart = list()

# is_admin = False
is_admin = user['username'] == 'admin'


@app.route('/')
@app.route('/index')
def index():

    # username = current_user.username

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


# API.

@app.route('/api/v1/new_item', methods=['POST'])
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

    # TODO: Store new item in db...

    item = Item(title=req_json['title'],
                description=req_json.get('description', ""),
                data_added=today(),
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
def api_update_item(item_id):
    """
    Update parameters of the stored item.
    :param item_id:
    :return:
    """
    idxs = [idx for (idx, item) in enumerate(db_items) if item['id'] == item_id]
    if len(idxs) != 1:
        abort(404)
    item_idx = idxs[0]

    req_json = request.json
    if not req_json:
        abort(400)
    if 'title' in req_json and type(req_json['title']) != str:
        abort(400)
    if 'description' in req_json and type(req_json['description']) != str:
        abort(400)

    db_items[item_idx]['title'] = req_json.get('title', db_items[item_idx]['title'])
    db_items[item_idx]['description'] = req_json.get('description', db_items[item_idx]['description'])

    return jsonify(task=db_items[item_idx])


@app.route('/api/v1/all_items', methods=['GET'])
def api_all_items():
    """
    List all items in the store.
    :return:
    """
    items = [get_item_json(item) for item in Item.query.all()]
    res = jsonify(items=items)
    return res


def is_exist(username, email):
    username_query = User.query.filter_by(username=username).first()
    email_query = User.query.filter_by(email=email).first()
    if username_query is None and email_query is None:
        return False
    return True


@app.route('/api/v1/register', methods=['POST'])
def api_register():
    """
    `username, password, birth_date, register_date, email, phone_number`
    :return:
    """
    data = request.json

    if not data:
        abort(400)
    for p in ['username', 'password', 'register_date', 'email', 'phone_number', 'birth_date']:
        if (p not in data) or type(data[p]) != str:
            abort(400)

    if is_exist(data['username'], data['email']):
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


@app.route('/api/v1/get_item/<int:item_id>', methods=['GET'])
def api_get_item(item_id):
    """
    Returns information related to item with id `item_id`.
    :param item_id:
    :return:
    """
    idxs = [idx for (idx, item) in enumerate(db_items) if item['id'] == item_id]
    if len(idxs) != 1:
        abort(404)
    item_idx = idxs[0]

    res = jsonify(db_items[item_idx])

    return res


@app.route('/api/v1/add_cart', methods=['POST'])
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
