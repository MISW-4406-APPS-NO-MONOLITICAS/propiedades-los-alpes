from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db: SQLAlchemy = SQLAlchemy()


# Init db with mysql
def init_db(app: Flask):
    databse_uri = os.environ.get("SQLALCHEMY_DATABASE_URI")
    if not databse_uri:
        databse_uri = "mysql+mysqldb://root:root@127.0.0.1:3306/listados"

    app.config["SQLALCHEMY_DATABASE_URI"] = databse_uri
    app.config["SQLACLHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    global db
    db.init_app(app)
