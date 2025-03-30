from .database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime

class User(db.Model, UserMixin):
  # required for flask security
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)
  fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
  active = db.Column(db.Boolean, nullable=False, default=True)

  # Relationship to Role model
  profile = db.relationship('ProfessionalProfile', backref=db.backref('user', cascade='all, delete'), uselist=False, lazy = True)
  roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', cascade='all, delete'), lazy=True)

class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  description = db.Column(db.String)

class UserRoles(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable = False)
  role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), nullable = False)

class ProfessionalProfile(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable = False)
  service_id = db.Column(db.Integer, db.ForeignKey('service.id', ondelete='CASCADE'), nullable = False)
  description = db.Column(db.String)
  date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
  experience = db.Column(db.Integer, nullable=False)
  service_pincodes = db.Column(db.String, nullable=False)
  status = db.Column(db.Enum('pending', 'approved', 'rejected'), nullable=False, default='pending')

  # Relationships
  service_requests = db.relationship('ServiceRequest', backref='professional', lazy = True, cascade='all, delete-orphan')
  reviews = db.relationship('Review', backref='professional', lazy=True, cascade='all, delete-orphan')

class Service(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  base_price = db.Column(db.Float, nullable=False)
  time_required = db.Column(db.Integer, nullable=False)
  description = db.Column(db.String)

  # Relationships
  professionals = db.relationship('ProfessionalProfile', backref='service', lazy=True, cascade='all, delete-orphan')
  service_requests = db.relationship('ServiceRequest', backref='service', lazy=True, cascade='all, delete-orphan')

class ServiceRequest(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  service_id = db.Column(db.Integer, db.ForeignKey('service.id', ondelete = 'CASCADE'), nullable = False)
  customer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), nullable = False)
  professional_id = db.Column(db.Integer, db.ForeignKey('professional_profile.id', ondelete = 'CASCADE'), nullable = False)
  address = db.Column(db.String, nullable = False)
  date_of_request = db.Column(db.DateTime, default = datetime.now, nullable = False)
  date_of_completion = db.Column(db.DateTime)
  status = db.Column(db.Enum('requested', 'accepted', 'completed', 'rejected', 'closed', name = 'service_status'), default = 'requested', nullable = False)
  remarks = db.Column(db.Text)
  customer_contact_number = db.Column(db.String, nullable = False)

  # relationships
  review = db.relationship('Review', uselist = False, backref = 'service_request', lazy = True, cascade = 'all, delete-orphan')

class Review(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id', ondelete = 'CASCADE'), nullable = False)
  customer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), nullable = False)
  professional_id = db.Column(db.Integer, db.ForeignKey('professional_profile.id', ondelete = 'CASCADE'), nullable = False)
  rating = db.Column(db.Enum('1', '2', '3', '4', '5', name = 'rating'), nullable = False)
  review = db.Column(db.Text)