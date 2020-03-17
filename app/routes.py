from flask import render_template, abort, jsonify, g, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app

user = {'username': 'test'}
# user = {'username': 'admin'}

db_items = list()

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

@app.route('/api/new_item', methods=['POST'])
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


@app.route('/api/update_item/<int:item_id>', methods=['PUT'])
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


@app.route('/api/all_items', methods=['GET'])
def api_all_items():
    """
    List all items in the store.
    :return:
    """

    res = jsonify({'items': db_items})
    return res
