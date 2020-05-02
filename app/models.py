from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from datetime import datetime, timedelta
import base64
import os

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id пользователя
    username = db.Column(db.String(64), index=True, unique=True)  # Имя пользователя
    email = db.Column(db.String(120), index=True, unique=True)  # Почта
    birth_date = db.Column(db.String(15))  # Дата рождения
    register_date = db.Column(db.String(15))  # Дата регистрации
    password_hash = db.Column(db.String(128))  # Хеш пароля
    phone_number = db.Column(db.String(15))  # Номер телефона
    token = db.Column(db.String(32), index=True, unique=True)  # Токен
    token_expiration = db.Column(db.DateTime)  # Дата инвалидации токена

    cart = db.relationship('Association')  # Корзина пользователя
    orders = db.relationship('Order', backref='user', lazy=True)  # Список заказов

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=1000000):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        db.session.commit()
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id товара
    title = db.Column(db.String(32))  # Название
    price = db.Column(db.Integer)  # Цена
    available = db.Column(db.Integer)  # Количество на складе
    category = db.Column(db.String(32), index=True)  # Категория
    description = db.Column(db.Text)  # Описание
    date_added = db.Column(db.String(15))  # Дата добавления


class Association(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # id пользователя
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)  # id товара
    amount = db.Column(db.Integer)  # Количество товара в корзине

    item = db.relationship('Item')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id заказа
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # id пользователя
    checkout_date = db.Column(db.String(15))  # Дата заказа
    finished = db.Column(db.Integer)  # True or False
    items = db.relationship('AssociationOrder')  # Предметы, входящие в заказ


class AssociationOrder(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)  # id заказа
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)  # id товара
    amount = db.Column(db.Integer)  # Количество заказанного товара

    item = db.relationship('Item')

