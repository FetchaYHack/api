from flask import Flask
from config import Config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, errors, api
app.register_blueprint(api.api_bp, url_prefix='/api')
