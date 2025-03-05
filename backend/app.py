from flask import Flask
from application.database import db
from application.models import User, Role
from application.config import LocalDevelopmentConfig
from application.api import api
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS

def create_app():
  app = Flask(__name__)

  CORS(app, supports_credentials=True)

  app.config.from_object(LocalDevelopmentConfig)
  
  db.init_app(app)

  datastore = SQLAlchemyUserDatastore(db, User, Role)
  app.security = Security(app, datastore=datastore, register_blueprint=False)

  app.app_context().push()

  return app

app = create_app()

from application import create_initial_data
from application import user_management_api
from application import service_management_api

api.init_app(app)

if __name__ == "__main__":
  app.run()