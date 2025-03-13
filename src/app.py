from flask import Flask
from flask_cors import CORS
from config import config
from db_config import db
from routes import register_blueprints

app = Flask(__name__)

CORS(app)

app.config.from_object(config['development'])

db.init_app(app)

register_blueprints(app)

if __name__ == '__main__':
    app.config.from_object(config['development'])
    with app.app_context():
        db.create_all()
    app.run()
