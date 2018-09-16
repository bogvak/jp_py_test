import pytest

from service import item_service, shopping_list_service, sl_items_service
from core import db_utils
from app import app

# Main run
db_utils.db.init_app(app)
app.app_context().push()
db_utils.init_db()

@pytest.fixture
def test_data():
    """ Insert test data to test
    """
    [item_service.insert_new_item(name) for name in ['Bread', 'Coka', 'Cokamber']]
    [shopping_list_service.insert_new_shoppingList(title,store) for title,store in [('#1',"Lego"),('Birhtday',''),('AliExpress','Ali')]]
    [sl_items_service.insert_sl_item(sl_id, item_id) for sl_id, item_id in [(3, 2), (3, 3), (4, 1),(4, 2),(1, 4)]]


class TestItemClass(object):
    """ Test class for basic testing Items business models
    """

    @pytest.mark.parametrize("name", ['New PyTest 1', 'New Item 2', 'Tomato'])
    def test_create_item(self, name):
        item_service.insert_new_item(name)

    def test_get_all_items(self):
        assert len(item_service.get_items()) == 3

    def test_get_item_by_id(self):
        assert item_service.get_item_by_id(3).name == "Tomato"

    def test_get_item_by_name_one(self):
        assert item_service.get_item_by_name("Tomato")[0].name == "Tomato"

    def test_get_item_by_name_many(self):
        assert len(item_service.get_item_by_name("New")) == 2

    def test_get_item_by_name_none(self):
        assert len(item_service.get_item_by_name("Rurur")) == 0

    def test_delete_item(self):
        item_service.delete_item(3)
        assert len(item_service.get_items()) == 2

    def test_update_item(self):
        item_service.update_item(2,"Updated Item Name")
        assert item_service.get_item_by_id(2).name == "Updated Item Name"

class TestShoppingListClass(object):
    """ Test class for basic testing Shopping Lists business models
    """

    @pytest.mark.parametrize("name, store", [("#1 Shopping", "Rimi"), ("Shopping #2", "Tiger")])
    def test_create_sl(self, name, store):
        shopping_list_service.insert_new_shoppingList(name, store)

    def test_create_sl_nostore(self):
        shopping_list_service.insert_new_shoppingList("Just a general Shopping List")

    def test_get_all_sl(self):
        assert len(shopping_list_service.get_sl()) == 3

    def test_get_sl_by_id(self):
        assert shopping_list_service.get_shoppingList_by_id(3).title == "Just a general Shopping List"

    def test_get_sl_by_title_one(self):
        assert shopping_list_service.get_shoppingList_by_title("Just a general Shopping List")[0].title == "Just a general Shopping List"

    def test_get_sl_by_title_one_len(self):
        assert len(shopping_list_service.get_shoppingList_by_title("Shopping")) == 3

    def test_delete_sl(self):
        shopping_list_service.delete_shoppingList(3)
        assert len(shopping_list_service.get_sl()) == 2

    def test_update_sl(self):
        new_id = shopping_list_service.insert_new_shoppingList("Just a general Shopping List").id
        shopping_list_service.update_shoppingList(new_id, title="Updated cool Shopping list", store="Maxima")
        assert shopping_list_service.get_shoppingList_by_id(new_id).title == "Updated cool Shopping list"
        assert shopping_list_service.get_shoppingList_by_id(new_id).storeName == "Maxima"
        shopping_list_service.update_shoppingList(new_id, store="Sportmaster")
        assert shopping_list_service.get_shoppingList_by_id(new_id).storeName == "Sportmaster"

class TestShoppingListItemsClass(object):
    """ Test class for basic testing of item operations in Shopping Lists
    """

    @pytest.mark.parametrize("sl_id, item_id, quantity", [(1, 1, 2), (1, 2, 4), (1, 3, 2), (2, 3, 1), (2, 2, 1)])
    def test_create_sl_item(self, sl_id, item_id, quantity):
        sl_items_service.insert_sl_item(sl_id,item_id,quantity)

    def test_get_sl_item(self):
        assert (sl_items_service.get_sl_item(1,1)).quantity == 2

    def test_get_sl_item_by_sl_id(self):
        assert len(sl_items_service.get_sl_item_by_sl_id(1)) == 2

    def test_add_sl_item_quantity(self):
        sl_items_service.insert_sl_item(1,1,4)
        assert (sl_items_service.get_sl_item(1, 1)).quantity == 6

    def test_get_sl_item_that_not_exist(self):
        assert sl_items_service.get_sl_item(3, 2) == None

    def test_update_sl_item_quantity(self):
        sl_items_service.update_sl_item(2, 2, 7)
        assert sl_items_service.get_sl_item(2, 2).quantity == 7

    def test_delete_sl_item(self):
        sl_items_service.delete_sl_item(1, 3)
        assert sl_items_service.get_sl_item(1, 3) == None

    def test_delete_all_sl_items(self):
        sl_items_service.delete_all_sl_items(1)
        assert len(sl_items_service.get_sl_item_by_sl_id(1)) == 0

    def test_delete_shopping_list_with_items(self):
        sl_items_service.insert_sl_item(3, 1)
        sl_items_service.insert_sl_item(3, 2)
        sl_items_service.insert_sl_item(3, 3)
        assert len(sl_items_service.get_sl_item_by_sl_id(3)) == 2
        shopping_list_service.delete_shoppingList(3)
        assert len(sl_items_service.get_sl_item_by_sl_id(3)) == 0

    def test_full_delete_item(self):
        item_service.delete_item(2)
        assert len(sl_items_service.get_sl_item_by_item_id(2)) == 0

class TestAdditionalTests(object):
    """ Some of additional tests
    """
    def test_test_data_fixture(self, test_data):
        pass

    def test_get_shoppingList_by_item_name(self):
        print(shopping_list_service.get_shoppingList_by_item_name("Coka"))
        print(shopping_list_service.get_shoppingList_by_item_name("New"))
        pass