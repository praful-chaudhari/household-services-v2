from flask_restful import Resource, reqparse
from .api import api
from flask import current_app as app
from flask_security import SQLAlchemyUserDatastore, verify_password, auth_required, current_user, login_user, logout_user

user_datastore : SQLAlchemyUserDatastore = app.security.datastore

# class CustomerRegisterResource(Resource):
#   def post(self):
#     parser = reqparse.RequestParer()
#     parser.add_argument('name')
#     parser.add_argument('email')
#     parser.add_argument('password')
#     data = parser.parse_args()

#     if user_datastore.find_user(email = data["email"]):
#       return {
#         "message": "Email already exists"
#       }, 409
    
#     user_datastore.create_user(name = data["name"], email = data["email"], password = data["password"], roles = ["customer"])
#     return {
#       "message": "Registration successful!"
#     }, 201

# class ProfessionalRegisterResource(Resource):
#   def post(self):
#     parser = reqparse.RequestParer()
#     parser.add_argument('name', required = True, help = "Name is required")
#     parser.add_argument('email', required = True, help = "Email is required")
#     parser.add_argument('password', required = True, help = "Password is required")
#     data = parser.parse_args()

#     if user_datastore.find_user(email = data["email"]):
#       return {
#         "message": "Email already exists"
#       }, 409
    
#     user_datastore.create_user(name = data["name"], email = data["email"], password = data["password"], roles = ["professional"])
#     return {
#       "message": "Registration successful!"
#     }, 201


class LoginResource(Resource):
  def __init__(self):
    self.parser = reqparse.RequestParser()
    self.parser.add_argument('email')
    self.parser.add_argument('password')

  def post(self):
    data = self.parser.parse_args()

    user = user_datastore.find_user(email = data["email"])
    if not user:
      return {
        "message": "Invalid email"
      }, 404
      
    if not verify_password(data["password"], user.password):
      return {
        "message": "Invalid password"
      }, 401
    
    if current_user.is_authenticated and current_user.id == user.id:
      logout_user()
    login_user(user)
    roles = [role.name for role in user.roles]
    return {
      "message": "Login successful!",
      "token": user.get_auth_token(),
      "roles": roles
    }, 200

api.add_resource(LoginResource, '/login')
# api.add_resource(CustomerRegisterResource, '/register/customer')
# api.add_resource(ProfessionalRegisterResource, '/register/professional')