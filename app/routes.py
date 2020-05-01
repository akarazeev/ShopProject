from flask import abort, jsonify, g, request
from flask_httpauth import HTTPBasicAuth

from app.models import User, Item, Association, Order, AssociationOrder
from app.utils import today, get_item_json, get_index_of_item
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

    new_user = User(
        username=data['username'],
        birth_date=data['birth_date'],
        register_date=data['register_date'],
        email=data['email'],
        phone_number=data['phone_number']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message='user added successfully'), 200


@app.route('/api/v1/token')
@auth.login_required
def get_auth_token():
    token = g.user.get_token()
    return jsonify(token=token)


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
    data = request.json
    if not data:
        abort(400)

    for p in ['item_id', 'amount']:
        if p not in data:
            abort(400)

    item = Item.query.filter_by(id=data['item_id']).first()
    if item is None:
        abort(400)

    user = g.user
    if user is None:
        abort(400)

    idx = get_index_of_item(user, item.id)
    amount = int(data['amount'])
    new_amount = amount
    if idx == -1:
        a = Association(amount=amount)
        a.item = item
        user.cart.append(a)
    else:
        user.cart[idx].amount += amount
        new_amount = user.cart[idx].amount

    db.session.add(user)
    db.session.commit()

    # TODO: Может так лучше?
    record = {
        'user_id': user.id,
        'item_id': data['item_id'],
        'amount': new_amount
    }
    # record = {
    #     'user_id': user.id,
    #     'item_id': data['item_id'],
    #     'amount': data['amount']
    # }
    return jsonify(record=record), 201


# TODO: Needs to be fixed ;)
@app.route('/api/v1/remove_cart', methods=['POST'])
@auth.login_required
def api_remove_cart():
    """
    Decrease item's amount in cart by one.
    :return:
    """
    data = request.json
    if not data:
        abort(400)

    for p in ['item_id']:
        if p not in data:
            abort(400)

    item = Item.query.filter_by(id=data['item_id']).first()
    if item is None:
        abort(400)

    user = g.user
    if user is None:
        abort(400)

    idx = get_index_of_item(user, item.id)
    if idx != -1:
        if user.cart[idx].amount > 1:
            user.cart[idx].amount -= 1
        # else:
        # TODO: Remove item completely from cart

        db.session.add(user)
        db.session.commit()

        record = {
            'user_id': user.id,
            'item_id': data['item_id'],
            'amount': data['amount']
        }
        return jsonify(record=record), 201
    else:
        return jsonify(text="no such item in cart"), 400


@app.route('/api/v1/cart', methods=['GET'])
@auth.login_required
def api_cart():
    """
    List all items in the cart of the user.
    :return:
    """
    # data = request.json
    user = g.user
    if user is None:
        abort(404)
    cart = [{'item': get_item_json(item.item), 'amount': item.amount} for item in user.cart]

    res = jsonify(cart=cart)
    return res


@app.route('/api/v1/cart/<int:user_id>', methods=['GET'])
@auth.login_required
def api_cart_userid(user_id):
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


@app.route('/api/v1/confirm_cart', methods=['POST'])
@auth.login_required
def api_confirm_order():
    """
    Confirm the order with items in cart and clear the cart.
    :return:
    """
    user = g.user
    if user is None:
        abort(404)
    cart = [{'item': get_item_json(item.item), 'amount': item.amount} for item in user.cart]

    # TODO: Needs to be fixed ;)
    order = Order(user_id=user, finished=0, checkout_date=today())
    # db.session.add(order)
    # db.session.commit()

    # TODO: Needs to be fixed too ;)
    cart_items = [
        {'item_id': get_item_json(item.item)['id'], 'amount': item.amount} for item in user.cart
    ]
    for item in cart_items:
        association_order = AssociationOrder(item_id=item['item_id'], amount=item['amount'], order_id=order.id)
        # db.session.add(association_order)
        # db.session.commit()

    # TODO: Clear the cart!

    return jsonify(text="order confirmed"), 201
