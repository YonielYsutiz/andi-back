from flask_sqlalchemy import SQLAlchemy
import pymysql

db = SQLAlchemy()

pymysql.install_as_MySQLdb()