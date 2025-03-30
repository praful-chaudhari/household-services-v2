from flask_restful import Resource, reqparse, fields, marshal
from .api import api
from flask import current_app as app, request
from .database import db
from .models import ProfessionalProfile, Review, ServiceRequest
from flask_caching import Cache
from flask_security import SQLAlchemyUserDatastore, verify_password, hash_password, auth_token_required, roles_required, current_user, login_user, logout_user, roles_accepted
from datetime import datetime

user_datastore : SQLAlchemyUserDatastore = app.security.datastore

cache = app.cache

login_user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'active': fields.Boolean,
    'roles': fields.List(fields.String),
    'authToken': fields.String
}

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'active': fields.Boolean,
    'roles': fields.List(fields.String),
    'timestamp': fields.DateTime
}

login_professional_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'active': fields.Boolean,
    'roles': fields.List(fields.String),
    'authToken': fields.String,
    'service_id': fields.Integer,
    'description': fields.String,
    'experience': fields.Integer
}

professional_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'email': fields.String,
  'active': fields.Boolean,
  'service': fields.Nested({
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'base_price': fields.Float,
    'time_required': fields.Integer
  }),
  'description': fields.String,
  'date_created': fields.DateTime,
  'experience': fields.Float,
  'service_pincodes': fields.String,
  'status': fields.String,
  'rating': fields.Float,
  'timestamp': fields.DateTime
}

class CustomerResource(Resource):

  @auth_token_required
  @roles_required('admin')
  @cache.cached(timeout = 300, key_prefix = lambda: f'customers{request.path}')
  def get(self, id = None):
    if id:
      customer = user_datastore.find_user(id=id)
      if customer:
        roles = [role.name for role in customer.roles]
        if 'customer' not in roles:
          return {'message': f'User with ID {id} is not customer'}, 404
        serialized_user = {
          'id': customer.id,
          'name': customer.name,
          'email': customer.email,
          'active': customer.active,
          'roles': roles,
          'timestamp': datetime.now()
        }
        return marshal(serialized_user, user_fields), 200
      return {'message': 'Customer not found'}, 404
    customers = user_datastore.user_model.query.filter(user_datastore.user_model.roles.any(name='customer')).all()
    final_customers = []
    for customer in customers:
      roles = [role.name for role in customer.roles]
      serialized_user = {
          'id': customer.id,
          'name': customer.name,
          'email': customer.email,
          'active': customer.active,
          'roles': roles,
          'timestamp': datetime.now()
        }
      final_customers.append(serialized_user)
    return marshal(final_customers, user_fields), 200
      

  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('name')
    parser.add_argument('email')
    parser.add_argument('password')
    data = parser.parse_args()

    if user_datastore.find_user(email = data["email"]):
      return {
        "message": "Email already exists"
      }, 409
    
    user_datastore.create_user(name = data["name"], email = data["email"], password = hash_password(data["password"]), roles = ["customer"])
    try:
      db.session.commit()
      if cache.delete('customers/customers'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      if cache.delete(f'customers{request.path}'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
    except:
      db.session.rollback()
      return {
        "message": "An error occurred while registering"
      }, 500
    return {
      "message": "Registration successful!"
    }, 201
  
  @auth_token_required
  @roles_required('admin')
  def patch(self, id = None):
    if not id:
      return {
        "message": "ID is required"
      }, 400
    user = user_datastore.find_user(id = id)
    if not user:
      return {
        "message": "User not found"
      }, 404
    roles = [role.name for role in user.roles]
    if 'customer' not in roles:
      return {
        "message": f"User with ID {id} is not a customer"
      }, 404
    
    parser = reqparse.RequestParser()
    parser.add_argument('name', type = str)
    parser.add_argument('email', type = str)
    parser.add_argument('active', type = bool)
    data = parser.parse_args()

    if data["name"]:
      user.name = data["name"]
    if data["email"]:
      if user_datastore.find_user(email = data['email']):
        return {
          "message": "Email already exists"
        }, 409
      user.email = data["email"]
    if data["active"] is not None:
      user.active = data["active"]
    try:
      db.session.commit()
      if cache.delete('customers/customers'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      if cache.delete(f'customers{request.path}'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
    except:
      db.session.rollback()
      return {
        "message": "An error occurred while updating"
      }, 500
    return {
      "message": "Customer updated successfully"
    }, 200
  
  @auth_token_required
  @roles_required('admin')
  def delete(self, id = None):
    if not id:
      return {
        "message": "ID is required"
      }, 400
    user = user_datastore.find_user(id = id)
    if not user:
      return {
        "message": "User not found"
      }, 404
    roles = [role.name for role in user.roles]
    if 'customer' not in roles:
      return {
        "message": f"User with ID {id} is not a customer"
      }, 404
    try:
      db.session.delete(user)
      db.session.commit()
      if cache.delete('customers/customers'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      if cache.delete(f'customers{request.path}'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
    except:
      db.session.rollback()
      return {
        "message": "An error occured while deleting customer"
      }, 500
    return {
      "message": "Customer deleted successfully"
    }, 200

class ProfessionalResource(Resource):

  @auth_token_required
  @roles_accepted('admin', 'customer')
  @cache.cached(timeout = 300, key_prefix = lambda: f'professionals{request.path}')
  def get(self, id = None):
    if id:
      user = user_datastore.find_user(id=id)
      if not user:
        return {'message': 'Professional not found'}, 404
      roles = [role.name for role in user.roles]
      if 'professional' not in roles:
        return {'message': f'User with ID {id} is not professional'}, 404
      profile = user.profile
      service = profile.service
      reviews = Review.query.filter_by(professional_id = id).all()
      rating = 0
      if len(reviews) > 0:
        rating = sum([int(review.rating) for review in reviews]) / len(reviews)
      
      serializable_professional = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'active': user.active,
        'service': service,
        'description': profile.description,
        'date_created': profile.date_created,
        'experience': profile.experience,
        'service_pincodes': profile.service_pincodes,
        'status': profile.status,
        'rating': rating,
        'timestamp': datetime.now()
      }
      return marshal(serializable_professional, professional_fields), 200
      
    professionals = user_datastore.user_model.query.filter(user_datastore.user_model.roles.any(name='professional')).all()
    if len(professionals) <= 0:
      return [], 200
    final_professionals = []
    for professional in professionals:
      roles = [role.name for role in professional.roles]
      if 'professional' not in roles:
        continue
      profile = professional.profile
      service = profile.service
      reviews = Review.query.filter_by(professional_id = professional.id).all()
      rating = 0
      if len(reviews) > 0:
        rating = sum([int(review.rating) for review in reviews]) / len(reviews)
          
      serializable_professional = {
        'id': professional.id,
        'name': professional.name,
        'email': professional.email,
        'active': professional.active,
        'service': service,
        'description': profile.description,
        'date_created': profile.date_created,
        'experience': profile.experience,
        'service_pincodes': profile.service_pincodes,
        'status': profile.status,
        'rating': rating,
        'timestamp': datetime.now()
      }
      final_professionals.append(serializable_professional)
    return marshal(final_professionals, professional_fields), 200


  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required = True, help = "Name is required")
    parser.add_argument('email', required = True, help = "Email is required")
    parser.add_argument('password', required = True, help = "Password is required")
    parser.add_argument('serviceId', required = True, help = "Service type is required")
    parser.add_argument('experience', required = True, help = "Experience is required")
    parser.add_argument('description', required = True, help = "Description is required")
    parser.add_argument('pincodes', required = True, help = "Pincodes are required")
    data = parser.parse_args()

    if user_datastore.find_user(email = data["email"]):
      return {
        "message": "Email already exists"
      }, 409
    
    user = user_datastore.create_user(name = data["name"], email = data["email"], password = hash_password(data["password"]), roles = ["professional"])
    try:
      db.session.commit()
      if cache.delete('professionals/professionals'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      if cache.delete(f'professionals{request.path}'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
    except:
      db.session.rollback()
      return {
        "message": "An error occurred while registering"
      }, 500
    profile = ProfessionalProfile(user_id = user.id, service_id = data["serviceId"], experience = data["experience"], description = data["description"], service_pincodes = data["pincodes"])
    try:
      db.session.add(profile)
      db.session.commit()
    except:
      db.session.rollback()
      db.session.delete(user)
      db.session.commit()
      if cache.delete('professionals/professionals'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      if cache.delete(f'professionals{request.path}'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      return {
        "message": "An error occurred while registering"
      }, 500
    return {
      "message": "Registration successful!"
    }, 201
  
  @auth_token_required
  @roles_required('admin')
  def patch(self, id = None):
    if not id:
      return {
        "message": "ID is required"
      }, 400
    user = user_datastore.find_user(id = id)
    if not user:
      return {
        "message": "User not found"
      }, 404
    roles = [role.name for role in user.roles]
    if 'professional' not in roles:
      return {
        "message": f"User with ID {id} is not a professional"
      }, 404
    profile = user.profile
    parser = reqparse.RequestParser()
    parser.add_argument('experience', type = int)
    parser.add_argument('description', type = str)
    parser.add_argument('status', type = str)
    parser.add_argument('active', type = bool)
    data = parser.parse_args()

    if data["experience"]:
      profile.experience = data["experience"] is not None
    if data["description"]:
      profile.description = data["description"]
    if data["status"]:
      profile.status = data["status"]
      user.active = data["status"] == 'approved'
    if data["active"] is not None:
      user.active = data["active"]
    try:
      db.session.commit()
      if cache.delete('professionals/professionals'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      if cache.delete(f'professionals{request.path}'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
    except:
      db.session.rollback()
      return {
        "message": "An error occurred while updating"
      }, 500
    return {
      "message": "Professional updated successfully"
    }, 200
  
  @auth_token_required
  @roles_required('admin')
  def delete(self, id = None):
    if not id:
      return {
        "message": "ID is required"
      }, 400
    user = user_datastore.find_user(id = id)
    if not user:
      return {
        "message": "User not found"
      }, 404
    roles = [role.name for role in user.roles]
    if 'professional' not in roles:
      return {
        "message": f"User with ID {id} is not a professional"
      }, 404
    profile = user.profile
    try:
      db.session.delete(profile)
      db.session.delete(user)
      db.session.commit()
      if cache.delete('professionals/professionals'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      if cache.delete(f'professionals{request.path}'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
    except:
      db.session.rollback()
      return {
        "message": "An error occured while deleting"
      }, 500
    return {
      "message": "Professional deleted successfully"
    }, 200


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
    
    if not user.active:
      return {
        "message": "User is not active"
      }, 401
      
    if not verify_password(data["password"], user.password):
      return {
        "message": "Invalid password"
      }, 401
    
    if current_user.is_authenticated and current_user.id == user.id:
      logout_user()
    login_user(user)
    roles = [role.name for role in user.roles]
    if 'professional' in roles:
      serialized_user = {}
      serialized_user['id'] = user.id
      serialized_user['name'] = user.name
      serialized_user['email'] = user.email
      serialized_user['roles'] = roles
      serialized_user['authToken'] = user.get_auth_token()
      serialized_user['service_id'] = user.profile.service_id
      serialized_user['description'] = user.profile.description
      serialized_user['active'] = user.active
      serialized_user['experience'] = user.profile.experience
      return marshal(serialized_user, login_professional_fields), 200
    else:
      serialized_user = {}
      serialized_user['id'] = user.id
      serialized_user['name'] = user.name
      serialized_user['email'] = user.email
      serialized_user['roles'] = roles
      serialized_user['active'] = user.active
      serialized_user['authToken'] = user.get_auth_token()
      return marshal(serialized_user, login_user_fields), 200
  
class ProfileResource(Resource):
  @auth_token_required
  def patch(self, id = None):
    if not id:
      return {
        "message": "ID is required"
      }, 400
    if current_user.id != id:
      return {
        "message": "You are not authorized to update this profile"
      }, 403
    user = user_datastore.find_user(id = id)
    if not user:
      return {
        "message": "User not found"
      }, 404
    parser = reqparse.RequestParser()
    parser.add_argument('name', type = str)
    parser.add_argument('oldPassword', type = str)
    parser.add_argument('newPassword', type = str)
    parser.add_argument('service_id', type = int)
    parser.add_argument('description', type = str)
    data = parser.parse_args()
    
    if data["name"]:
      user.name = data["name"]
    if data["oldPassword"]:
      if not verify_password(data["oldPassword"], user.password):
        return {
          "message": "Invalid old password"
        }, 401
      user.password = hash_password(data["newPassword"])
    if user.has_role('professional'):
      profile = user.profile
      if data["service_id"]:
        profile.service_id = data["service_id"]
      if data["description"]:
        profile.description = data["description"]
      try:
        db.session.commit()
        if user.has_role('professional'):
          if cache.delete('professionals/professionals'):
            print("Cache deleted successfully")
          else:
            print("Cache not found")
          if cache.delete(f'professionals/professionals/{id}'):
            print("Cache deleted successfully")
          else:
            print("Cache not found")
        else:
          if cache.delete('customers/customers'):
            print("Cache deleted successfully")
          else:
            print("Cache not found")
          if cache.delete(f'customers/customers/{id}'):
            print("Cache deleted successfully")
          else:
            print("Cache not found")
      except:
        db.session.rollback()
        return {
          "message": "An error occurred while updating"
        }, 500
    return {
      "message": "Profile updated successfully"
    }, 200

api.add_resource(LoginResource, '/login')
api.add_resource(CustomerResource, '/customer/register', '/customers', '/customers/<int:id>')
api.add_resource(ProfessionalResource, '/professional/register', '/professionals', '/professionals/<int:id>')
api.add_resource(ProfileResource, '/profile/<int:id>')