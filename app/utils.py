import datetime


def today():
    return str(datetime.datetime.now().date())


def get_item_json(item):
    return {'id': item.id,
            'title': item.title,
            'description': item.description,
            'date_added': item.date_added,
            'category': item.category}


def get_index_of_item(user, item_id):
    cart = user.cart
    for i in range(len(cart)):
        if cart[i].item.id == item_id:
            return i
    return -1
