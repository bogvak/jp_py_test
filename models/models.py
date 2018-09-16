from core import db_utils

db = db_utils.db

class ShoppingList(db.Model):
    """ Class describing realtionship : Shopping List -> Items
    """
    __tablename__ = 'slist'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    storeName = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)


