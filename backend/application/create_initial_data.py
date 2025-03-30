from flask import current_app as app
from .database import db
from .models import ProfessionalProfile, Service
from flask_security import SQLAlchemyUserDatastore, hash_password

with app.app_context():
  db.create_all()

  if not Service.query.filter_by(name = "Plumber").first():
    plumber = Service(name = "Plumber", base_price = 1000, time_required = 10, description = "Plumber")
    db.session.add(plumber)
    db.session.commit()

  user_datastore : SQLAlchemyUserDatastore = app.security.datastore

  user_datastore.find_or_create_role(name="admin", description="Super user")
  user_datastore.find_or_create_role(name="customer", description="Customer")
  user_datastore.find_or_create_role(name="professional", description="Service Provider")

  if not user_datastore.find_user(email = "admin@fixitfixit.com"):
    user_datastore.create_user(name = "Admin", email = "admin@fixitfixit.com", password = hash_password("admin123"), roles = ["admin"])
  if not user_datastore.find_user(email = "customer@gmail.com"):
    user_datastore.create_user(name = "Customer", email = "customer@gmail.com", password = hash_password("cust1234"), roles = ["customer"])
  if not user_datastore.find_user(email = "professional@gmail.com"):
    user_datastore.create_user(name = "Professional", email = "professional@gmail.com", password = hash_password("prof1234"), roles = ["professional"])
    professional = user_datastore.find_user(email = "professional@gmail.com")
    professional_profile = ProfessionalProfile(user_id = professional.id, service_id = 1, description = "I am a professional", experience = 10, service_pincodes = "123456", status = "pending")
    db.session.add(professional_profile)

  db.session.commit()