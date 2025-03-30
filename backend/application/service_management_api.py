import time
from flask_restful import Resource, reqparse, fields, marshal_with, marshal
from .api import api
from .database import db
from flask import current_app as app, request
from .models import Service, ServiceRequest, ProfessionalProfile, Review
from .tasks import service_request_notification
from flask_security import SQLAlchemyUserDatastore, auth_token_required, roles_required, current_user, roles_accepted
from datetime import datetime

user_datastore : SQLAlchemyUserDatastore = app.security.datastore

cache = app.cache

class ServiceResource(Resource):
  service_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'base_price': fields.Float,
    'time_required': fields.Integer,
    'description': fields.String,
  }

  @marshal_with(service_fields)
  @cache.cached(timeout = 300, key_prefix = lambda: f'services{request.path}')
  def get(self, id = None):
    if id:
      service = Service.query.get(id)
      if service:
        return service, 200
      return {'message': 'Service not found'}, 404
    services = Service.query.all()
    return services, 200

  @auth_token_required
  @roles_required('admin')
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required = True, help = "Name is required")
    parser.add_argument('basePrice', required = True, help = "Base price is required")
    parser.add_argument('timeRequired', required = True, help = "Time required is required")
    parser.add_argument('description')
    data = parser.parse_args()

    service = Service(name = data["name"], base_price = data["basePrice"], time_required = data["timeRequired"], description = data["description"])
    try:
      db.session.add(service)
      db.session.commit()
      if cache.delete('services/services'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      if cache.delete(f'services{request.path}'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      return {'message': 'Service added successfully'}, 201
    except:
      db.session.rollback()
      return {'message': 'An error occurred while adding service'}, 500

  @auth_token_required
  @roles_required('admin')
  def patch(self, id = None):
    if not id:
      return {'message': 'Service ID is required'}, 400

    service = Service.query.get(id)
    if service:
      parser = reqparse.RequestParser()
      parser.add_argument('name')
      parser.add_argument('basePrice')
      parser.add_argument('timeRequired')
      parser.add_argument('description')
      data = parser.parse_args()

      service.name = data.get('name', service.name)
      service.base_price = data.get('basePrice', service.base_price)
      service.time_required = data.get('timeRequired', service.time_required)
      service.description = data.get('description', service.description)
      try:
        db.session.commit()
        if cache.delete('services/services'):
          print("Cache deleted successfully")
        else:
          print("Cache not found")
        if cache.delete(f'services{request.path}'):
          print("Cache deleted successfully")
        else:
          print("Cache not found")
        return {'message': 'Service edited successfully'}, 200
      except:
        db.session.rollback()
        return {'message': 'An error occurred while updating service'}, 500
    return {'message': 'Service not found'}, 404
  
  @auth_token_required
  @roles_required('admin')
  def delete(self, id = None):
    if not id:
      return {'message': 'Service ID is required'}, 400

    service = Service.query.get(id)
    if service:
      try:
        db.session.delete(service)
        db.session.commit()
        if cache.delete('services/services'):
          print("Cache deleted successfully")
        else:
          print("Cache not found")
        if cache.delete(f'services{request.path}'):
          print("Cache deleted successfully")
        else:
          print("Cache not found")
        return {'message': 'Service deleted successfully'}, 200
      except:
        db.session.rollback()
        return {'message': 'An error occurred while deleting service'}, 500
    return {'message': 'Service not found'}, 404
  
class ServiceRequestsResource(Resource):
  service_request_fields = {
    'id': fields.Integer,
    'service': fields.Nested({'id': fields.Integer, 'name': fields.String, 'base_price': fields.Float, 'time_required': fields.Integer, 'description': fields.String}),
    'customer': fields.Nested({'id': fields.Integer, 'name': fields.String, 'email': fields.String}),
    'professional': fields.Nested({'id': fields.Integer, 'name': fields.String, 'email': fields.String}),
    'status': fields.String,
    'date_of_request': fields.DateTime,
    'date_of_completion': fields.DateTime,
    'address': fields.String,
    'remarks': fields.String,
    'customer_contact_number': fields.String,
    'review': fields.Nested({'id': fields.Integer, 'rating': fields.String, 'review': fields.String})
  }

  @auth_token_required
  @cache.cached(timeout = 300, key_prefix = lambda: f'service_requests{request.path}')
  def get(self, id = None):
    if id:
      service_request = ServiceRequest.query.get(id)
      if not service_request:
        return {'message': 'Service request not found'}, 404
        
      customer = user_datastore.find_user(id = service_request.customer_id)
      professional = user_datastore.find_user(id = service_request.professional_id)
      profile = professional.profile
      service = profile.service
      review = Review.query.filter_by(service_request_id = service_request.id).first()

      serializable_service_request = {
        'id': service_request.id,
        'service': service,
        'customer': customer,
        'professional': {
          'id': professional.id,
          'name': professional.name,
          'email': professional.email,
          'service': service,
          'description': profile.description,
          'experience': profile.experience,
          'service_pincodes': profile.service_pincodes,
          'status': profile.status,
        },
        'status': service_request.status,
        'date_of_request': service_request.date_of_request,
        'date_of_completion': service_request.date_of_completion,
        'address': service_request.address,
        'remarks': service_request.remarks,
        'customer_contact_number': service_request.customer_contact_number,
        'review': review
      }

      if current_user.has_role('admin'):
        return marshal(serializable_service_request, self.service_request_fields), 200
      elif current_user.has_role('customer'):
        if service_request.customer_id == current_user.id:
          return marshal(serializable_service_request, self.service_request_fields), 200
      elif current_user.has_role('professional'):
        if service_request.professional_id == current_user.id:
          return marshal(serializable_service_request, self.service_request_fields), 200
      return {'message': 'Unauthorized'}, 403
    
    if current_user.has_role('admin'):
      service_requests = ServiceRequest.query.all()
    elif current_user.has_role('customer'):
      service_requests = ServiceRequest.query.filter_by(customer_id=current_user.id).all()
    elif current_user.has_role('professional'):
      service_requests = ServiceRequest.query.filter_by(professional_id=current_user.id).all()
    else:
      return {'message': 'Unauthorized'}, 403
    
    final_service_requests = []
    for service_request in service_requests:
      customer = user_datastore.find_user(id = service_request.customer_id)
      professional = user_datastore.find_user(id = service_request.professional_id)
      profile = professional.profile
      service = profile.service
      review = Review.query.filter_by(service_request_id = service_request.id).first()

      serializable_service_request = {
        'id': service_request.id,
        'service': service,
        'customer': customer,
        'professional': {
          'id': professional.id,
          'name': professional.name,
          'email': professional.email,
          'service': service,
          'description': profile.description,
          'experience': profile.experience,
          'service_pincodes': profile.service_pincodes,
          'status': profile.status,
        },
        'status': service_request.status,
        'date_of_request': service_request.date_of_request,
        'date_of_completion': service_request.date_of_completion,
        'address': service_request.address,
        'remarks': service_request.remarks,
        'customer_contact_number': service_request.customer_contact_number,
        'review': review
      }
      final_service_requests.append(serializable_service_request)
      
    return marshal(final_service_requests, self.service_request_fields), 200
  
  @auth_token_required
  @roles_required('customer')
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('service_id', required = True, help = "Service ID is required")
    parser.add_argument('professional_id', required = True, help = "Professional ID is required")
    parser.add_argument('address', required = True, help = "Address is required")
    parser.add_argument('remarks')
    parser.add_argument('customer_contact_number', required = True, help = "Customer contact number is required")
    data = parser.parse_args()

    service_request = ServiceRequest(service_id = data["service_id"], customer_id = current_user.id, professional_id = data["professional_id"], address = data["address"], remarks = data["remarks"], customer_contact_number = data["customer_contact_number"])
    try:
      db.session.add(service_request)
      db.session.commit()
      if cache.delete('service_requests/service-requests'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      if cache.delete(f'service_requests{request.path}'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      return {'message': 'Service request added successfully'}, 201
    except:
      db.session.rollback()
      return {'message': 'An error occurred while adding service request'}, 500
  
  @auth_token_required
  @roles_accepted('professional', 'customer', 'admin')
  def patch(self, id = None):
    if not id:
      return {'message': 'Service request ID is required'}, 400
    
    service_request = ServiceRequest.query.get(id)
    
    if not service_request:
      return {'message': 'Service request not found'}, 404
    
    customer = user_datastore.find_user(id = service_request.customer_id)
    
    if current_user.has_role('professional'):
      if service_request.professional_id != current_user.id:
        return {'message': 'Unauthorized'}, 403
      
      parser = reqparse.RequestParser()
      parser.add_argument('status', required = True, help = "Status is required")
      data = parser.parse_args()

      service_request.status = data["status"]
      try:
        db.session.commit()
        if cache.delete('service_requests/service-requests'):
          print("Cache deleted successfully")
        else:
          print("Cache not found")
        if cache.delete(f'service_requests{request.path}'):
          print("Cache deleted successfully")
        else:
          print("Cache not found")
        service_request_notification.delay(customer.name, service_request.status)
        return {'message': 'Service request status updated successfully'}, 200
      except:
        db.session.rollback()
        return {'message': 'An error occurred while updating service request status'}, 500
    elif current_user.has_role('customer'):
      if service_request.customer_id != current_user.id:
        return {'message': 'Unauthorized'}, 403
      
      parser = reqparse.RequestParser()
      parser.add_argument('status', required = True, help = "Status is required")
      data = parser.parse_args()

      service_request.status = data["status"]
      service_request.date_of_completion = datetime.now()
      try:
        db.session.commit()
        if cache.delete('service_requests/service-requests'):
          print("Cache deleted successfully")
        else:
          print("Cache not found")
        if cache.delete(f'service_requests{request.path}'):
          print("Cache deleted successfully")
        else:
          print("Cache not found")
        service_request_notification.delay(customer.name, service_request.status)
        return {'message': 'Service request status updated successfully'}, 200
      except:
        db.session.rollback()
        return {'message': 'An error occurred while updating service request status'}, 500
    elif current_user.has_role('admin'):
      parser = reqparse.RequestParser()
      parser.add_argument('status', required = True, help = "Status is required")
      data = parser.parse_args()

      service_request.status = data["status"]
      try:
        db.session.commit()
        if cache.delete('service_requests/service-requests'):
          print("Cache deleted successfully")
        else:
          print("Cache not found")
        if cache.delete(f'service_requests{request.path}'):
          print("Cache deleted successfully")
        else:
          print("Cache not found")
        service_request_notification.delay(customer.name, service_request.status)
        return {'message': 'Service request status updated successfully'}, 200
      except:
        db.session.rollback()
        return {'message': 'An error occurred while updating service request status'}, 500


class ReviewResource(Resource):
  review_fields = {
    'id': fields.Integer,
    'service_request_id': fields.Integer,
    'customer_id': fields.Integer,
    'professional_id': fields.Integer,
    'rating': fields.String,
    'review': fields.String,
    'timestamp': fields.DateTime
  }

  @auth_token_required
  @cache.cached(timeout = 300, key_prefix = lambda: f'reviews{request.path}')
  def get(self, id = None):
    if id:
      if current_user.has_role('customer'):
        reviews = Review.query.filter_by(customer_id = current_user.id).all()
      elif current_user.has_role('professional'):
        reviews = Review.query.filter_by(professional_id = current_user.id).all()
      else:
        return {'message': 'Unauthorized'}, 403
      if len(reviews) <= 0:
        return [], 200
      serialized_reviews = []
      for review in reviews:
        serialized_reviews.append({
          'id': review.id,
          'service_request_id': review.service_request_id,
          'customer_id': review.customer_id,
          'professional_id': review.professional_id,
          'rating': review.rating,
          'review': review.review,
          'timestamp': datetime.now()
        })
      return marshal(serialized_reviews, self.review_fields), 200
    
    elif not current_user.has_role('admin'):
      return {'message': 'Unauthorized'}, 403
    
    reviews = Review.query.all()
    serialized_reviews = []
    for review in reviews:
      serialized_reviews.append({
        'id': review.id,
        'service_request_id': review.service_request_id,
        'customer_id': review.customer_id,
        'professional_id': review.professional_id,
        'rating': review.rating,
        'review': review.review,
        'timestamp': datetime.now()
      })
    return marshal(serialized_reviews, self.review_fields), 200
  
  @auth_token_required
  @roles_required('customer')
  def post(self, id = None):
    if not id:
      return {
        "message": "ID is required"
      }, 400
    parser = reqparse.RequestParser()
    parser.add_argument('rating', required = True, help = "Rating is required")
    parser.add_argument('comment', required = True, help = "Comment is required")
    data = parser.parse_args()
    service_request = ServiceRequest.query.get(id)
    if not service_request:
      return {
        "message": "Service request not found"
      }, 404
    review = Review(service_request_id = id, customer_id = service_request.customer_id, professional_id = service_request.professional_id, rating = data["rating"], review = data["comment"])
    service_request.status = 'closed'
    service_request.date_of_completion = datetime.now()
    try:
      db.session.add(review)
      db.session.commit()
      if cache.delete('reviews/reviews'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      if cache.delete(f'reviews{request.path}'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      if cache.delete('service_requests/service-requests'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      if cache.delete(f'service_requests/service-requests/{id}'):
        print("Cache deleted successfully")
      else:
        print("Cache not found")
      return {
        "message": "Review added successfully"
      }, 201
    except:
      db.session.rollback()
      return {
        "message": "An error occurred while adding review"
      }, 500

api.add_resource(ServiceResource, '/services', '/services/<int:id>')
api.add_resource(ServiceRequestsResource, '/service-requests', '/service-requests/<int:id>')
api.add_resource(ReviewResource, '/reviews', '/reviews/<int:id>')