## Quick install

Assumed that Python 3 and `pipenv` already installed

```shell
git clone https://github.com/bogvak/jp_py_test.git
cd jp_py_test
pipenv --three
pipenv shell
pipenv install
py app.py
```

Now API is available on `http://localhost:5000` address.

All endpoints are documented with Swagger UI standard.

------

## Test

```shell
pytest -s
```

To pass integrations test, you need to have main application run.

------

## Used frameworks

- Flask
- Flask-RESTPlus (https://flask-restplus.readthedocs.io/en/stable/)
- Flask-SQLAlchemy (http://flask-sqlalchemy.pocoo.org/2.3/)
- Requests

------

## Used resources

- Official frameworks documentation
- A lot of StackOverflow answers