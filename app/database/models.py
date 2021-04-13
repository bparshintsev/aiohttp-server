from .mixin import MixinCRUD

from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float


__all__ = [
    'Base',
    'User',
    'Order',
    'UserRelation'
]


Base = declarative_base()


class User(Base, MixinCRUD):
    __tablename__ = 'users'
    _hidden = {'password', 'nickname'}

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    family_name = Column(String)
    nickname = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"Пользователь {self.last_name} {self.first_name}"


class UserRelation(Base, MixinCRUD):
    __tablename__ = 'users_relations'

    id = Column(Integer, primary_key=True)
    src_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dst_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    src_user = relationship("User", foreign_keys=[src_user_id])
    dst_user = relationship("User", foreign_keys=[src_user_id])


class OrderProduct(Base, MixinCRUD):
    __tablename__ = 'orders_products'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    order = relationship("Order", foreign_keys=[order_id], back_populates='products')
    product = relationship("Product", foreign_keys=[product_id], back_populates='orders')


class Order(Base, MixinCRUD):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', foreign_keys=[user_id], backref="orders")
    products = relationship('OrderProduct', back_populates='order')


class Product(Base, MixinCRUD):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)

    orders = relationship("OrderProduct", back_populates='product')
