from .extensions import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from flask_security.models import fsqla_v3 as fsqla

fsqla.FsModels.set_db_info(db)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String, nullable=False)
    # Relationships
    roles = db.relationship('Role', secondary='user_roles')
    user_ebook_associations = db.relationship('UserEbookAssociation', back_populates='user', cascade="delete")

    @property
    def ebooks_requested(self):
        return UserEbookAssociation.query.filter_by(user_id=self.id, request_status='requested').count()
    
    @property
    def ebooks_issued(self):
        return UserEbookAssociation.query.filter_by(user_id=self.id, request_status='issued').count()

    @property
    def ebooks_purchased(self):
        return UserEbookAssociation.query.filter_by(user_id=self.id, request_status='purchased').count()

    def is_max_ebooks_limit(self):
        issued_ebooks = UserEbookAssociation.query.filter_by(user_id=self.id, request_status='issued').count()
        requested_ebooks = UserEbookAssociation.query.filter_by(user_id=self.id, request_status='requested').count()
        if issued_ebooks + requested_ebooks >= 5:
            return True
        else:
            return False

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))



class Ebook(db.Model):
    __tablename__ = 'ebook'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    authors = db.Column(db.String, nullable=False)
    acces_duration = db.Column(db.Integer, default=7)
    price = db.Column(db.Integer)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    # Relationships
    section = db.relationship('Section', back_populates='ebooks')
    user_ebook_associations = db.relationship('UserEbookAssociation', back_populates='ebook', cascade="delete")

    @property
    def section_name(self):
        return self.section.name

    @property
    def average_rating(self):
        associations = self.user_ebook_associations
        ratings = [association.rating for association in associations if association.rating is not None]
        if ratings:
            return round(sum(ratings) / len(ratings), 1)
        return None




class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    # Relationships
    ebooks = db.relationship('Ebook', back_populates='section', cascade="delete")

    @property
    def total_ebooks(self):
        return len(self.ebooks)



class UserEbookAssociation(db.Model):
    __tablename__ = 'user_ebook_association'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebook.id', ondelete='CASCADE'))
    date_issued = db.Column(db.DateTime)
    date_return = db.Column(db.DateTime)
    request_status = db.Column(db.String)
    rating = db.Column(db.Integer())
    # Relationships
    user = db.relationship('User', back_populates='user_ebook_associations')
    ebook = db.relationship('Ebook', back_populates='user_ebook_associations')

    @property
    def user_email(self):
        return self.user.email

    @property
    def section_name(self):
        return self.ebook.section.name
    
    @property
    def ebook_name(self):
        return self.ebook.name

    @property
    def ebook_authors(self):
        return self.ebook.authors
    