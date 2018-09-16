from flask import Flask
from api import api
from core import db_utils

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api.api.init_app(app)
db_utils.db.init_app(app)
app.app_context().push()

if __name__ == '__main__':
    app.run(debug=True)
