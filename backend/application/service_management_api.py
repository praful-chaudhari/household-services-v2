from flask_restful import Resource, reqparse, fields, marshal_with
from .api import api
from .database import db
from .models import Service
from flask_security import auth_token_required, roles_required

class ServiceResource(Resource):
  service_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'base_price': fields.Float,
    'time_required': fields.Integer,
    'description': fields.String,
  }

  @marshal_with(service_fields)
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
    parser.add_argument('base_price', required = True, help = "Base price is required")
    parser.add_argument('time_required', required = True, help = "Time required is required")
    parser.add_argument('description')
    data = parser.parse_args()

    service = Service(name = data["name"], base_price = data["base_price"], time_required = data["time_required"], description = data["description"])
    try:
      db.session.add(service)
      db.session.commit()
      return {'message': 'Service added successfully'}, 201
    except:
      db.session.rollback()
      return {'message': 'An error occurred while adding service'}, 500

api.add_resource(ServiceResource, '/services', '/services/<int:id>')