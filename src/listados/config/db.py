from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = None

# Init db with mysql
def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:root@127.0.0.1:3306/listados'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    global db
    db = SQLAlchemy(app)