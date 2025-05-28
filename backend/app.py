from flask import Flask
from flask_cors import CORS
from application.config import Config
from application.extensions import db, security, cache
from application.resources import api
from application.models import User, Role
from flask_security import SQLAlchemyUserDatastore
from application.create_initial_data import create_data

from application.worker import celery_init_app
import flask_excel as excel
from application.tasks import send_return_date_reminder, revoke_expired_access, monthly_report
from celery.schedules import crontab

app = None
celery_app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    cache.init_app(app)
    db.init_app(app)
    api.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)
    app.app_context().push()
    
    return app

app = create_app()
celery_app = celery_init_app(app)
excel.init_excel(app)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every evening at 5:00 p.m.
    sender.add_periodic_task(
        crontab(hour=17, minute=0),
        send_return_date_reminder.s(),
    )
    # Executes every evening at 5:00 p.m.
    sender.add_periodic_task(
        crontab(hour=17, minute=0),
        revoke_expired_access.s(),
    )
    # Executes every 1st of the month at 5:00 p.m.
    sender.add_periodic_task(
        crontab(day_of_month=1, hour=0, minute=0),
        monthly_report.s(),
    )


with app.app_context():
        user_datastore = security.datastore
        db.create_all()
        create_data(user_datastore)

from application.routes import *

# creating random data for testing purposes

# from application.create_initial_data import create_random_users, create_random_ebooks, create_random_user_ebooks, create_random_sections, create_expired_association
# create_random_sections(3)
# create_random_users(security.datastore, 20)
# create_random_ebooks(10)
# create_random_user_ebooks(10)
# create_expired_association(user_id=2)



if __name__ == '__main__':
    app.run()


# terminal 1
# ~/go/bin/MailHog


# terminal 2
# cd frontend && npm install && npm run serve
# cd frontend && npm run serve


# terminal 3
# cd backend && virtualenv venv && source venv/bin/activate && pip install -r requirements.txt && python app.py
# cd backend && source venv/bin/activate && python app.py


# terminal 4
# cd backend && source venv/bin/activate && celery -A app:celery_app worker -l INFO


# terminal 5
# cd backend && source venv/bin/activate && celery -A app:celery_app beat -l INFO
