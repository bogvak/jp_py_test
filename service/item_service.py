""" Business logic for Items operations.
"""

from models import models
from core import db_utils
from service import sl_items_service

def get_items() -> list:
    """Get all items

        Args:
            id: Item ID.

        Returns:
            List of Items

    """
    return models.Item.query.all()


def get_item_by_id(id: int) -> models.Item:
    """Get one item by its ID

    Args:
        id: Item ID.

    Returns:
        Item

    """
    return models.Item.query.get(id)


def get_item_by_name(name: str) -> list:
    """Get one item by its ID

    Args:
        id: Item name (keywords)

    Returns:
        Item

    """
    results = models.Item.query.filter(models.Item.name.like('%%%s%%' % name)).all()
    return results


def insert_new_item(_name: str) -> models.Item:
    """Insert new Item

    Args:
        id: Item ID.

    Returns:
        Item

    """
    new_item = models.Item(name=_name)
    db_utils.add_and_save_db(new_item)
    return new_item


def delete_item(id: int) -> bool:
    """Delete item

    Args:
        id: Item ID.

    Returns:
        None - if nothing to delete, True - if Item deleted

    """
    item = get_item_by_id(id)
    if item == None:
        return None
    sl_items_service.delete_all_items(id)
    db_utils.delete_from_db(item)
    return True


def update_item(id: int, name: str) -> models.Item:
    """Update item

    Args:
        id: Item ID.
        id: Item name.

    Returns:
        Item or None - if Item is not exists

    """
    item = get_item_by_id(id)
    if item == None:
        return None
    item.name = name
    db_utils.save_db()
    return item