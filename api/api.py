from flask_restplus import Api, Resource, fields
from service import item_service, sl_items_service, shopping_list_service

api = Api()

item = api.namespace('item', description='Item operations')
sl = api.namespace('sl', description='Shopping lists operations')


# General Item marshalling model
item_model = api.model('Item', {
    'id': fields.Integer(readOnly=True, description='Item unique identifier'),
    'name': fields.String(required=True, description='Item name')
})

# Item marshalling model for creating item and item operations
item_model_data = api.model('Item Data', {
    'name': fields.String(required=True, description='Item name')
})

# General Shopping List marshaling model
shopping_list_model = api.model('Shopping List', {
    'id': fields.Integer(readOnly=True, description='Shopping List unique identifier'),
    'title': fields.String(required=True, description='Shopping List Title'),
    'storeName': fields.String(description='Store name'),
    'date_created': fields.DateTime(description='Date created')
})

# Shopping List marshaling model for creating and SL operations
shopping_list_model_data = api.model('Shopping List Data', {
    'title': fields.String(required=True, description='Shopping List Title'),
    'store': fields.String(description='Store name')
})

# Marshaling model list of Items with quantity
shopping_list_items = api.model('Shopping List Items', {
    'id': fields.Integer(description='Item ID'),
    'name': fields.String(description='Item name'),
    'quantity': fields.Integer(description='Item quantity')
})

# Marshaling model for inserting of Items to Shopping List
shopping_list_items_insert = api.model('Shopping List Item Insert', {
    'id': fields.Integer(required=True, description='Item ID'),
    'name': fields.String(description='Item name, if new'),
    'quantity': fields.Integer(
        description='Item quantity: added to current id exists and positive, reduced - if negative and deleted if quantity become zero or less')
})

# Marshaling model for deletinf of Shopping Lists
shopping_list_items_delete = api.model('Shopping List Item Delete', {
    'id': fields.Integer(required=True, description='Item ID')
})

@item.errorhandler
def no_item(error):
    """Namespace error handler
    """

    return {'message': "something goes wrong"}, getattr(error, 'code', 500)


@item.route('/')
class ItemList(Resource):
    """ Endpoint Resource for item list and inserting of new items
    """

    @item.doc('Get all known items')
    @item.marshal_list_with(item_model)
    def get(self):
        """  Return all items
        """
        return item_service.get_items()

    @item.doc('Insert new Item')
    @item.expect(item_model_data)
    @item.marshal_with(item_model, code=201)
    def post(self):
        """  Insert new item
        """
        return item_service.insert_new_item(api.payload['name']), 201


@item.route('/name/<string:name>')
class ItemListByName(Resource):
    """ Endpoint Resource for getting items by name
    """

    @item.doc('Get all known items')
    @item.marshal_list_with(item_model)
    def get(self, name):
        """ Return all items with some keyword
        """
        return item_service.get_item_by_name(name)


@item.route('/<int:id>')
class ItemOne(Resource):
    """ Endpoint Resource for item operations
    """

    @item.marshal_list_with(item_model)
    def get(self, id):
        """ Return items with ID
        """
        item = item_service.get_item_by_id(id)
        if item is None:
            api.abort(404, "Item {} doesn't exist".format(id))
        return item

    @item.doc('Update item with ID')
    @item.param('name', 'Name of item')
    @item.expect(item_model_data)
    @item.marshal_list_with(item_model)
    def put(self, id):
        """ Update item with ID
        """
        if not "name" in api.payload:
            api.abort(400, 'Not enough of parameters')
        if api.payload['name'] == "":
            api.abort(400, "Name of Item couldn't be empty")
            pass
        item = item_service.update_item(id, api.payload['name'])
        if item is None:
            api.abort(404, "Item {} doesn't exist".format(id))
        return item_service.update_item(id, api.payload['name'])

    @item.doc('Delete item with ID')
    def delete(self, id):
        """ Delete Item with ID
        """
        result = item_service.delete_item(id)
        if result:
            return '', 204
        api.abort(404, "Item {} doesn't exist".format(id))


@item.route('/<int:id>/shoplists')
class ItemInShoppingLists(Resource):
    """ Endpoint Resource for getting of shopping lists list for one Item
    """

    @sl.marshal_list_with(shopping_list_model)
    def get(self, id):
        """ Return all shopping lists those contains Item
        """
        sl = sl_items_service.get_shoplist_for_item(id)
        return sl


@sl.route('/')
class ShoppingListsList(Resource):
    """ Endpoint Resource for getting of shopping lists list and creating new Shopping lists
    """

    @sl.doc('Get all Shopping lists')
    @sl.marshal_list_with(shopping_list_model)
    def get(self):
        """ Return all shopping lists
        """
        return shopping_list_service.get_sl()

    @sl.doc('Insert new Shopping List')
    @sl.expect(shopping_list_model_data)
    @sl.marshal_with(shopping_list_model, code=201)
    def post(self):
        """ Insert new Shopping List
        """
        print(api.payload['title'])
        return shopping_list_service.insert_new_shoppingList(api.payload['title'],
                                                             api.payload.get("store", "")), 201


@sl.route('/<int:id>')
class ShoppingLists(Resource):
    """ Endpoint Resource for Shopping Lists operations
    """

    @sl.doc(id='get_shopping_list')
    @sl.marshal_list_with(shopping_list_model)
    def get(self, id):
        """ Return shopping list with some ID
        """
        sl = shopping_list_service.get_shoppingList_by_id(id)
        if sl is None:
            api.abort(404, "Shopping list {} doesn't exist".format(id))
        return sl

    @sl.doc('Update Shopping List with some ID')
    @sl.expect(shopping_list_model_data)
    @sl.marshal_list_with(shopping_list_model)
    def put(self, id):
        """ Update shopping list with some ID
        """
        if not "title" in api.payload:
            api.abort(400, 'Not enough of parameters')
        if api.payload['title'] == "":
            api.abort(400, "Title of shopping list couldn't be empty")
            pass
        if 'store' in api.payload:
            sl = shopping_list_service.update_shoppingList(id, title=api.payload['title'], store=api.payload['store'])
        else:
            sl = shopping_list_service.update_shoppingList(id, title=api.payload['title'])
        if item is None:
            api.abort(404, "Shopping list {} doesn't exist".format(id))
        return sl

    @sl.doc('Delete shopping list with ID')
    @sl.response(204, 'Shopping List deleted')
    @sl.response(404, 'Shopping List not found')
    def delete(self, id):
        """ Delete shopping list with some ID
        """
        result = shopping_list_service.delete_shoppingList(id)
        if result:
            return '', 204
        api.abort(404, "Shopping list {} doesn't exist".format(id))


@sl.route('/title/<string:title>')
class ShoppingListsByTitle(Resource):
    """ Endpoint Resource for searching of Shopping lists by Title
    """

    @sl.doc(id='get_shopping_list_by_title')
    @sl.marshal_list_with(shopping_list_model)
    def get(self, title):
        """ Return list of Shoppping Lists those title contains keyword
        """
        sl = shopping_list_service.get_shoppingList_by_title(title)
        return sl


@sl.route('/itemname/<string:name>')
class ShoppingListsByItemname(Resource):
    """ Endpoint Resource for searching of Shopping lists by item name
    """

    @sl.doc(id='get_shopping_list_by_itemname')
    @sl.marshal_list_with(shopping_list_model)
    def get(self, name):
        """ Return list of Shoppping Lists with items those names are contains keywords
        """
        sl = shopping_list_service.get_shoppingList_by_item_name(name)
        return sl


@sl.route('/<int:sl_id>/item')
class ShoppingListItems(Resource):
    """ Endpoint Resource for getting of items in one shopping list
    """

    @sl.doc('Get all items for one shopping list')
    @sl.marshal_list_with(shopping_list_items)
    def get(self, sl_id):
        """ Return all items for one shopping list
        """
        return sl_items_service.get_items_in_shopping_list(sl_id)

    @sl.doc('Insert new Item')
    @sl.expect(shopping_list_items_insert)
    @sl.marshal_list_with(shopping_list_items, code=201)
    def post(self, sl_id):
        """ Insert item to shopping list
        """
        result = sl_items_service.insert_sl_item(_sl_id=sl_id, _item_id=api.payload['id'],
                                                 _quantity=api.payload.get('quantity', 1))
        if result == "Bad item":
            api.abort(404, "Item {} doesn't exist".format(api.payload['id']))
        if result == "Bad SL":
            api.abort(404, "Shopping List {} doesn't exist".format(sl_id))
        sl_updated = sl_items_service.get_items_in_shopping_list(sl_id)
        if sl_updated:
            return sl_updated, 201

    @sl.doc('Delete Item From Shopping List')
    @sl.expect(shopping_list_items_delete)
    @sl.marshal_list_with(shopping_list_items, code=201)
    def delete(self, sl_id):
        """ Insert item from shopping list
        """
        sl_items_service.delete_sl_item(_sl_id=sl_id, _item_id=api.payload.get('id', -1))
        sl_updated = sl_items_service.get_items_in_shopping_list(sl_id)
        if sl_updated:
            return sl_updated, 201
        api.abort(404, "Shopping list {} doesn't exist".format(sl_id))
