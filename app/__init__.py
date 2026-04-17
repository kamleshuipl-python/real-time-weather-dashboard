from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes, models

app.register_blueprint(routes.main)