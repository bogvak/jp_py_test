import pytest

from service import shopping_list_service
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
    [shopping_list_service.insert_new_shoppingList(title,store) for title,store in [('#1',"Lego"),('Birhtday',''),('AliExpress','Ali')]]


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