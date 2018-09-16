import pytest
import requests

def test_items_get():
    r = requests.get('http://localhost:5000/item')
    res = r.json()
    assert (type(res) == list)

def test_create_new_shopping_list():
    r = requests.post('http://localhost:5000/sl/', json={'title':'Test Shopping List'})
    print(r.json())