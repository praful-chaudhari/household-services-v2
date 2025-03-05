from flask import current_app as app
from .database import db
from flask_security import SQLAlchemyUserDatastore, hash_password

with app.app_context():
  db.create_all()

  user_datastore : SQLAlchemyUserDatastore = app.security.datastore

  user_datastore.find_or_create_role(name="admin", description="Super user")
  user_datastore.find_or_create_role(name="customer", description="Customer")
  user_datastore.find_or_create_role(name="professional", description="Service Provider")

  if not user_datastore.find_user(email = "admin@iitm.in"):
    user_datastore.create_user(name = "Admin", username = "admin", email = "admin@iitm.in", password = hash_password("admin123"), roles = ["admin"])
  if not user_datastore.find_user(email = "cust@iitm.in"):
    user_datastore.create_user(name = "Customer", username = "customer", email = "cust@iitm.in", password = hash_password("user1234"), roles = ["customer"])
  if not user_datastore.find_user(email = "professional@iitm.in"):
    user_datastore.create_user(name = "Professional", username = "professional", email = "professional@iitm.in", password = hash_password("professional"), roles = ["professional"])

  db.session.commit()