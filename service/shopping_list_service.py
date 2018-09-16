# Shopping List model business logic
from models import models
from core import db_utils
from datetime import datetime
from service import sl_items_service
from service import item_service


def get_sl() -> list:
    """Get all shopping lists

    Args:
        Nothing

    Returns:
        List of shopping lists

    """
    return models.ShoppingList.query.all()


def get_shoppingList_by_id(id: int) -> models.ShoppingList:
    """Get shopping list by ID

    Args:
        Shopping list ID

    Returns:
        Shopping list

    """
    return models.ShoppingList.query.get(id)


def get_shoppingList_by_title(title: str) -> list:
    """Get shopping list by title

    Args:
        Shopping list title

    Returns:
        List of shopping lists

    """
    results = models.ShoppingList.query.filter(models.ShoppingList.title.like('%%%s%%' % title)).all()
    return results


def get_shoppingList_by_item_name(name: str) -> list:
    """Get shopping list by item name

    Args:
        Item name

    Returns:
        List of shopping lists

    """
    items_ = item_service.get_item_by_name(name)
    if len(items_) > 0:
        shoppping_lists_ids = set()
        for item_ in items_:
            sls_for_next_id = sl_items_service.get_sl_item_by_item_id(item_.id)
            for next_sl in sls_for_next_id:
                shoppping_lists_ids.add(next_sl.sl_id)
        shoppping_lists_obj = []
        for next_id in shoppping_lists_ids:
            shoppping_lists_obj.append(get_shoppingList_by_id(next_id))
        return shoppping_lists_obj


def insert_new_shoppingList(_title: str, store: str = "") -> models.ShoppingList:
    """Insert new shopping list

    Args:
        Shopping list title
        Shopping list title - not required

    Returns:
        List of shopping lists

    """
    new_sl = models.ShoppingList(title=_title, storeName=store, date_created=datetime.now())
    db_utils.add_and_save_db(new_sl)
    return new_sl


def delete_shoppingList(id: int) -> bool:
    """Delete shopping list

    Args:
        Shopping list IDd

    Returns:
        Bool

    """
    sl = get_shoppingList_by_id(id)
    if sl:
        sl_items_service.delete_all_sl_items(id)
        db_utils.delete_from_db(sl)
        return True
    else:
        return False


def update_shoppingList(id: int, **kwargs) -> models.ShoppingList:
    """Update shopping list

    Args:
        Shopping list ID
        store, title - not optional

    Returns:
        Shopping List

    """
    sl = get_shoppingList_by_id(id)
    sl.title = kwargs.get('title', sl.title)
    sl.storeName = kwargs.get('store', sl.storeName)
    db_utils.save_db()
    return sl
