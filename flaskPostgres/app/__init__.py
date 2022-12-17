from flask import Flask
from sqlalchemy import create_engine
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app: Flask = Flask(__name__)
db: SQLAlchemy = SQLAlchemy()
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


login = LoginManager(app)

from app.models import Employee, Post
from app import routes

# user_datastore = SQLAlchemyUserDatastore(db, Employee, Post)
# security = Security(app, user_datastore)



