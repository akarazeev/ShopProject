from flask import render_template, abort, jsonify, g, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
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
    if not req_json or not 'title' in req_json:
        abort(400)

    # TODO: Store new item in db...

    item = {
        'id': len(db_items),
        'title': req_json['title'],
        'description': req_json.get('description', ""),
        'date_added': "today"
    }
    db_items.append(item)

    return jsonify({'task': item}), 201


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

    return jsonify({'task': db_items[item_idx]})


@app.route('/api/v1/all_items', methods=['GET'])
def api_all_items():
    """
    List all items in the store.
    :return:
    """

    res = jsonify({'items': db_items})
    return res


def is_exist(username):
    cur_user = User.query.filter_by(username=username).first()
    if cur_user is None:
        return False
    return True


@app.route('/api/v1/register', methods=['POST'])
def api_register():
    """
    `username, password, birth_date, register_date, email, phone_number`
    :return:
    """
    data = request.json
    username = data['username']
    if is_exist(username):
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
    return jsonify({'message': 'user added successfully'}), 200


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
    if not req_json or not 'user_id' in req_json or not 'item_id' in req_json:
        abort(400)

    # TODO: Make a record in db...

    record = {
        'user_id': req_json['user_id'],
        'item_id': req_json['item_id']
    }
    db_cart.append(record)

    return jsonify({'record': record}), 201


@app.route('/api/v1/cart/<int:user_id>', methods=['GET'])
def api_cart(user_id):
    """
    List all items in the cart of user with id `user_id`.
    :return:
    """

    res = jsonify({'cart': db_cart})
    return res
