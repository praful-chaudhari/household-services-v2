from .database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime

class User(db.Model, UserMixin):
  # required for flask security
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  username = db.Column(db.String, unique=True, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)
  fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
  active = db.Column(db.Boolean, nullable=False, default=True)

  # Relationship to Role model
  roles = db.relationship('Role', secondary='user_roles', backref='users', lazy=True)

class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  description = db.Column(db.String)

class UserRoles(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
  role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))

class ProfessionalProfile(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
  service_id = db.Column(db.Integer, db.ForeignKey('service.id', ondelete='CASCADE'))
  description = db.Column(db.String)
  date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
  experience = db.Column(db.Integer, nullable=False)
  verified = db.Column(db.Boolean, nullable=False, default=False)

  # Relationships
  user = db.relationship('User', backref='professional_profile', lazy = True)
  service = db.relationship('Service', backref='professionals', lazy = True)
  service_requests = db.relationship('ServiceRequest', backref='professional', lazy = True)

class Service(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  base_price = db.Column(db.Float, nullable=False)
  time_required = db.Column(db.Integer, nullable=False)
  description = db.Column(db.String)

  # Relationships
  service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)

class ServiceRequest(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  service_id = db.Column(db.Integer, db.ForeignKey('service.id', ondelete = 'CASCADE'), nullable = False)
  customer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), nullable = False)
  professional_id = db.Column(db.Integer, db.ForeignKey('professional_profile.id', ondelete = 'CASCADE'))
  date_of_request = db.Column(db.DateTime, default = datetime.now, nullable = False)
  date_of_completion = db.Column(db.DateTime)
  status = db.Column(db.Enum('requested', 'assigned', 'rejected', 'closed', name = 'service_status'), default = 'requested', nullable = False)
  remarks = db.Column(db.Text)

  # relationships
  review = db.relationship('Review', uselist = False, backref = 'service_request', lazy = True, cascade = 'all, delete-orphan')

class Review(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id', ondelete = 'CASCADE'), nullable = False)
  customer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), nullable = False)
  rating = db.Column(db.Enum('1', '2', '3', '4', '5', name = 'rating'), nullable = False)
  review = db.Column(db.Text)