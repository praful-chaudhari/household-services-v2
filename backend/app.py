from flask import Flask
from application.database import db
from application.models import User, Role
from application.config import LocalDevelopmentConfig
from application.tasks import monthly_report, service_requests_reminder
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS
from application.celery_init import celery_init_app
from celery.schedules import crontab
from flask_caching import Cache

def create_app():
  app = Flask(__name__)

  CORS(app, supports_credentials=True)

  app.config.from_object(LocalDevelopmentConfig)
  
  db.init_app(app)

  cache = Cache(app)
  app.cache = cache

  datastore = SQLAlchemyUserDatastore(db, User, Role)

  app.security = Security(app, datastore=datastore, register_blueprint=False)

  app.app_context().push()

  return app

app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()

from application import create_initial_data
from application import user_management_api
from application import service_management_api
from application.routes import *

from application.api import api
api.init_app(app)

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.add_periodic_task(
    crontab(minute = "*/1"),
    monthly_report.s()
  )

@celery.on_after_finalize.connect
def send_service_requests_reminder(sender, **kwargs):
  sender.add_periodic_task(
    crontab(minute = "*/1"),
    service_requests_reminder.s()
  )

if __name__ == "__main__":
  app.run()



#            Example                                                          Meaning

# crontab()    -------------------------------------------------->  Execute every minute.

# crontab(minute=0, hour=0)   ----------------------------------->  Execute daily at midnight.

# crontab(minute=0, hour='*/3')   ------------------------------->  Execute every three hours: midnight, 3am, 6am, 9am, noon, 3pm, 6pm, 9pm.

# crontab(minute=0,hour='0,3,6,9,12,15,18,21')  ----------------->  Same as previous.

# crontab(minute='*/15')    ------------------------------------->  Execute every 15 minutes.

# crontab(day_of_week='sunday')   ------------------------------->  Execute every minute (!) at Sundays.

# crontab(minute='*',hour='*', day_of_week='sun')  -------------->  Same as previous.

# crontab(minute='*/10',hour='3,17,22', day_of_week='thu,fri') -->  Execute every ten minutes, but only between 3-4 am, 5-6 pm, and 10-11 pm on Thursdays or Fridays.

# crontab(minute=0, hour='*/2,*/3')   --------------------------->  Execute every even hour, and every hour divisible by three. This means: at every hour except: 1am, 5am, 7am, 11am, 1pm, 5pm, 7pm, 11pm

# crontab(minute=0, hour='*/5')   ------------------------------->  Execute hour divisible by 5. This means that it is triggered at 3pm, not 5pm (since 3pm equals the 24-hour clock value of “15”, which is divisible by 5).

# crontab(minute=0, hour='*/3,8-17')  --------------------------->  Execute every hour divisible by 3, and every hour during office hours (8am-5pm).

# crontab(0, 0, day_of_month='2')   ------------------------- --->  Execute on the second day of every month.

# crontab(0, 0, day_of_month='2-30/2')   ------------------------>  Execute on every even numbered day.

# crontab(0, 0,day_of_month='1-7,15-21')  ----------------------->  Execute on the first and third weeks of the month.

# crontab(0, 0, day_of_month='11',month_of_year='5')  ----------->  Execute on the eleventh of May every year.

# crontab(0, 0,month_of_year='*/3')   --------------------------->  Execute every day on the first month of every quarter.