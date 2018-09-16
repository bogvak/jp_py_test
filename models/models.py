from core import db_utils

db = db_utils.db

class Item_ShoppingList(db.Model):
    """ Class describing Shopping List DB model
    """
    __tablename__ = 'sl_item'

    sl_id = db.Column('sl_id', db.Integer, db.ForeignKey('slist.id'), primary_key=True)
    item_id = db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
    quantity = db.Column('quantity', db.Integer, nullable=False, default=1)


class Item(db.Model):
    """ Class describing Item DB models
    """
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    # shopping_lists = db.relationship('Item_ShoppingList', lazy=True, backref='items')


class ShoppingList(db.Model):
    """ Class describing realtionship : Shopping List -> Items
    """
    __tablename__ = 'slist'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    storeName = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)
    # items = db.relationship('Item_ShoppingList',  lazy=True, backref='shopping_lists')


