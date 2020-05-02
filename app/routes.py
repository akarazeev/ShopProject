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

    available = 0
    if 'amount' in req_json:
        available = int(req_json['amount'])

    item = Item(title=req_json['title'],
                description=req_json.get('description', ""),
                date_added=today(),
                category=req_json['category'],
                available=available)

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
    item.available = req_json.get('amount', item.available)

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

    record = {
        'user_id': user.id,
        'item_id': data['item_id'],
        'amount': new_amount
    }

    return jsonify(record=record), 201


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

    removing_items = 1
    if 'amount' in data:
        removing_items = int(data['amount'])

    item = Item.query.filter_by(id=data['item_id']).first()
    if item is None:
        abort(400)

    user = g.user
    if user is None:
        abort(400)

    idx = get_index_of_item(user, item.id)
    if idx != -1:
        if user.cart[idx].amount > removing_items:
            user.cart[idx].amount -= removing_items
        elif user.cart[idx].amount < removing_items:
            return jsonify(text="incorrect amount of removing items"), 400
        else:
            db.session.delete(user.cart[idx])
            db.session.commit()
            return jsonify(text="removed from cart"), 201

        db.session.add(user)
        db.session.commit()

        record = {
            'user_id': user.id,
            'item_id': data['item_id'],
            'amount': user.cart[idx].amount
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


@app.route('/api/v1/orders', methods=['GET'])
@auth.login_required
def api_orders():
    """
    List all orders of the user.
    :return:
    """
    # data = request.json
    user = g.user
    if user is None:
        abort(404)
    orders = [{'order': order.id} for order in user.orders]

    res = jsonify(orders=orders)
    return res


@app.route('/api/v1/order/<int:order_id>', methods=['GET'])
@auth.login_required
def api_orders_orderid(order_id):
    """
    List all items in the order with id `order_id`.
    :return:
    """
    user = g.user
    if user is None:
        abort(404)

    order = Order.query.filter_by(id=order_id).first()
    if order is None:
        return jsonify(text="no such order"), 400
    elif user.id != order.user_id:
        return jsonify(text="access denied"), 400
    else:
        items = [{'item': get_item_json(item.item), 'amount': item.amount} for item in order.items]
        res = dict(items=items, finished=order.finished, checkout_date=order.checkout_date)
        return jsonify(order=res), 201


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

    # create the order
    order = Order(user_id=user.id, finished=0, checkout_date=today())
    for elem in user.cart:
        association_order = AssociationOrder(amount=elem.amount)
        association_order.item = elem.item
        order.items.append(association_order)
    db.session.add(order)
    db.session.commit()

    # Clear the cart
    clear_cart(user)

    return jsonify(text="order confirmed"), 201


@app.route('/api/v1/categories', methods=['GET'])
def api_all_categories():
    """
    List all categories of the store items.
    :return:
    """
    query = db.session.query(Item.category.distinct().label('category'))
    categories = [row.category for row in query.all()]

    res = jsonify(categories=categories)
    return res, 201


@app.route('/api/v1/search', methods=['GET'])
def api_filter_items_by_category():
    """
    List all items of pointed category.
    :return:
    """
    data = request.json
    if not data or 'category' not in data:
        abort(400)

    category = data['category']
    items = Item.query.filter_by(category=category).all()
    items = [{'item': get_item_json(item), 'amount': item.available} for item in items]
    return jsonify(items=items), 201


def clear_cart(user):
    for elem in user.cart:
        db.session.delete(elem)
    db.session.commit()

