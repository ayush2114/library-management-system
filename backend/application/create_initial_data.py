from datetime import timedelta
from flask_security import SQLAlchemySessionUserDatastore
from flask_security.utils import hash_password
from .extensions import db
from .models import *

def create_data(user_datastore : SQLAlchemySessionUserDatastore):

    user_datastore.find_or_create_role(name='admin', description='Librarian')
    user_datastore.find_or_create_role(name='user', description='User')

    if not user_datastore.find_user(email='admin@abc.in'):
        user_datastore.create_user(
            email='admin@abc.in',
            password=hash_password('1234'),
            roles=['admin'],
            active=True
        )

    if not user_datastore.find_user(email='ayush@abc.in'):
        user_datastore.create_user(
            email='ayush@abc.in',
            password=hash_password('1234'),
            roles=['user'],
            active=True
        )

    db.session.commit()



# creating some random data for testing purposes

from faker import Faker

fake = Faker()

# creating some random n users
def create_random_users(user_datastore : SQLAlchemySessionUserDatastore, n):
    for _ in range(n):
        if not user_datastore.find_user(email=fake.email()):
            user_datastore.create_user(
                email=fake.email(),
                password=hash_password('1234'),
                roles=['user'],
                active=True
            )
    db.session.commit()

# creating some random n sections
def create_random_sections(n):
    for _ in range(n):
        name = fake.word()
        this_section = Section.query.filter_by(name=name).first()
        if this_section:
            continue
        description = fake.text()
        new = Section(name=name, description=description)
        db.session.add(new)
    db.session.commit()

# creating random n ebooks
def create_random_ebooks(n):
    for _ in range(n):
        name = fake.word()
        this_ebook = Ebook.query.filter_by(name=name).first()
        if this_ebook:
            continue
        authors = fake.name()
        content = fake.text()
        price = fake.random_int()
        section_id = fake.random_int(min=1, max=3)
        new = Ebook(name=name, authors=authors, content=content, price=price, section_id=section_id)
        db.session.add(new)
    db.session.commit()

# create random n user-ebook associations
def create_random_user_ebooks(n):
    for _ in range(n):
        user_id = fake.random_int(min=2, max=21)
        ebook_id = fake.random_int(min=1, max=10)
        this_association = UserEbookAssociation.query.filter_by(user_id=user_id, ebook_id=ebook_id).first()
        if this_association:
            continue

        new = UserEbookAssociation(user_id=user_id, ebook_id=ebook_id, request_status='requested')
        db.session.add(new)
    db.session.commit()

# create a association with expired return date
def create_expired_association(user_id):
    expired_ebook = Ebook(name='expired', authors='expired', content='expired', price=0, section_id=1)
    db.session.add(expired_ebook)
    db.session.commit()
    ebook_id = Ebook.query.filter_by(name='expired').first().id

    this_association = UserEbookAssociation.query.filter_by(user_id=user_id, ebook_id=ebook_id).first()
    if this_association:
        db.session.delete(this_association)

    new = UserEbookAssociation(user_id=user_id, ebook_id=ebook_id, request_status='issued', date_issued=datetime.utcnow(), date_return=datetime.utcnow() - timedelta(days=1))
    db.session.add(new)
    db.session.commit()