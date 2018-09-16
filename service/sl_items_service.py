# Shopping List Items model business logic
from models import models
from core import db_utils
from service import item_service, shopping_list_service


def get_sl_item(sl_id: int, item_id: int) -> models.Item_ShoppingList:
    """Get one item in Shopping List

    Args:
        Shopping list ID
        Item ID

    Returns:
        Item in Shopping List record

    """
    return models.Item_ShoppingList.query.get((sl_id, item_id))


def get_sl_item_by_sl_id(_sl_id: int) -> list:
    """Get all items records/IDs in Shopping List

    Args:
        Shopping list ID

    Returns:
        Lists of Shopping List -> Item records

    """
    return models.Item_ShoppingList.query.filter(models.Item_ShoppingList.sl_id == _sl_id).all()


def get_sl_item_by_item_id(_item_id: int) -> list:
    """Get all Shopping Lists records/IDs for one Item

    Args:
        Item ID

    Returns:
        Lists of Shopping List -> Item records

    """
    return models.Item_ShoppingList.query.filter(models.Item_ShoppingList.item_id == _item_id).all()


def get_shoplist_for_item(item_id: int) -> list:
    """Get all Shopping Lists objects for one Item

    Args:
        Item ID

    Returns:
        Shopping Lists list

    """
    sl_items = get_sl_item_by_item_id(item_id)
    sl_quantity = []
    for next_sl_item in sl_items:
        next_item = shopping_list_service.get_shoppingList_by_id(next_sl_item.sl_id)
        sl_quantity.append(dict(id=next_item.id, title=next_item.title, storeName=next_item.storeName,
                                date_created=next_item.date_created))
    print(sl_quantity)
    return sl_quantity


def get_items_in_shopping_list(sl_id: int):
    """Get all items records/IDs in Shopping List

    Args:
        Item ID

    Returns:
        Items list

    """
    sl_items = get_sl_item_by_sl_id(sl_id)
    items_quantity = []
    for next_sl_item in sl_items:
        next_item = item_service.get_item_by_id(next_sl_item.item_id)
        items_quantity.append(dict(id=next_item.id, name=next_item.name, quantity=next_sl_item.quantity))
    return items_quantity


def insert_sl_item(_sl_id: int, _item_id: int, _quantity: int =1):
    """Insert item to Shopping List

        Args:
            Shopping List ID
            Item ID
            _quantity - optional

        Returns:
            Item

    """
    check_item = item_service.get_item_by_id(_item_id)
    if not (check_item):
        return "Bad item"
    check_sl = shopping_list_service.get_shoppingList_by_id(_sl_id)
    if not (check_sl):
        return "Bad SL"
    new_item_in_sl = get_sl_item(_sl_id, _item_id)
    if new_item_in_sl == None:
        if _quantity > 0:
            new_item_in_sl = models.Item_ShoppingList(sl_id=_sl_id, item_id=_item_id, quantity=_quantity)
            db_utils.add_and_save_db(new_item_in_sl)
        else:
            return True
    else:
        new_item_in_sl.quantity = new_item_in_sl.quantity + _quantity
        if new_item_in_sl.quantity < 1:
            delete_sl_item(_sl_id, _item_id)
            return True
        db_utils.save_db()
    return new_item_in_sl


def update_sl_item(_sl_id, _item_id, _quantity):
    """Update item in Shopping List

        Args:
            Shopping List ID
            Item ID

        Returns:
            Item

    """
    item_in_sl = get_sl_item(_sl_id, _item_id)
    item_in_sl.quantity = _quantity
    db_utils.save_db()
    return item_in_sl


def delete_sl_item(_sl_id, _item_id):
    """Delete item in Shopping List

        Args:
            Shopping List ID
            Item ID

        Returns:
            Item

    """
    if _item_id < 0:
        return False
    item_in_sl = get_sl_item(_sl_id, _item_id)
    if item_in_sl:
        db_utils.delete_from_db(item_in_sl)


def delete_all_sl_items(_sl_id):
    """Delete all Items in Shopping List

        Args:
            Shopping List ID

        Returns:
            Lens of deleted Items

    """
    items_in_sl = get_sl_item_by_sl_id(_sl_id)
    for next_item in items_in_sl:
        db_utils.delete_from_db_no_commit(next_item)
    db_utils.save_db()
    return len(items_in_sl)


def delete_all_items(_item_id):
    """Delete all Items from Shopping Lists for one item

            Args:
                Shopping List ID

            Returns:
                Lens of deleted Items

        """
    items = get_sl_item_by_item_id(_item_id)
    for next_item in items:
        db_utils.delete_from_db_no_commit(next_item)
    db_utils.save_db()
    return len(items)
