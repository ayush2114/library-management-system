from flask_restful import Api, Resource, marshal_with, reqparse, fields
from flask_security import auth_required, roles_required
from .extensions import db, cache
from .exceptions import HTTPStatus
from .models import *

api = Api(prefix='/api')

Ebookfields = {
    'id': fields.Integer,
    'name': fields.String,
    'authors': fields.String,
    'content': fields.String,
    'price': fields.Integer,
    'section_id': fields.Integer,
    'acces_duration': fields.Integer,
    'section_name': fields.String,
    'average_rating': fields.Integer(default=None)
}

ebook_parser = reqparse.RequestParser()
ebook_parser.add_argument('name', type=str)
ebook_parser.add_argument('authors', type=str)
ebook_parser.add_argument('content', type=str)
ebook_parser.add_argument('price', type=int)
ebook_parser.add_argument('section_id', type=int)
ebook_parser.add_argument('acces_duration', type=int, default=7)


class EbookApi(Resource):

    @cache.cached(timeout=5)
    @auth_required('token')
    @marshal_with(Ebookfields)
    def get(self, ebook_id=None):
        if ebook_id:
            this_ebook = Ebook.query.filter_by(id=ebook_id).first()
            if this_ebook:
                return this_ebook, 200
            else:
                raise HTTPStatus(404, 'Ebook not found')
        else:
            all_ebooks = Ebook.query.all()
            if all_ebooks:
                return all_ebooks, 200
            else:
                raise HTTPStatus(404, 'No ebooks found')
    
    @auth_required('token')
    @roles_required('admin')
    def post(self):
        args = ebook_parser.parse_args()
        this_ebook = Ebook.query.filter_by(name=args['name']).first()
        if this_ebook:
            raise HTTPStatus(409, 'Ebook already exists')
        new_ebook = Ebook(name=args['name'], authors=args['authors'], content=args['content'], price=args['price'], section_id=args['section_id'], acces_duration=args['acces_duration'])
        db.session.add(new_ebook)
        db.session.commit()
        raise HTTPStatus(201, 'Ebook created succesfully')

    @auth_required('token')
    @roles_required('admin')
    def delete(self, ebook_id):
        this_ebook = Ebook.query.filter_by(id=ebook_id).first()
        if this_ebook:
            db.session.delete(this_ebook)
            db.session.commit()
            raise HTTPStatus(200, 'Ebook deleted successfully')
        else:
            raise HTTPStatus(404, 'Ebook not found')

    @auth_required('token')
    @roles_required('admin')
    def put(self, ebook_id):
        this_ebook = Ebook.query.filter_by(id=ebook_id).first()
        if this_ebook:
            args = ebook_parser.parse_args()
            this_ebook.name = args['name']
            this_ebook.authors = args['authors']
            this_ebook.content = args['content']
            this_ebook.price = args['price']
            this_ebook.section_id = args['section_id']
            this_ebook.acces_duration = args['acces_duration']
            db.session.commit()
            raise HTTPStatus(200, 'Ebook updated successfully')
        else:
            raise HTTPStatus(404, 'Ebook not found')

Sectionfields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'date_created': fields.DateTime,
    'total_ebooks': fields.Integer,
}

section_parser = reqparse.RequestParser()
section_parser.add_argument('name', type=str)
section_parser.add_argument('description', type=str)

class SectionApi(Resource):

    @cache.cached(timeout=5)
    @auth_required('token')
    @marshal_with(Sectionfields)
    def get(self, section_id=None):
        if section_id:
            this_section = Section.query.filter_by(id=section_id).first()
            if this_section:
                return this_section, 200
            else:
                raise HTTPStatus(404, 'Section not found')
        else:
            all_sections = Section.query.all()
            if all_sections:
                return all_sections, 200
            else:
                raise HTTPStatus(404, 'No sections found')
    
    @auth_required('token')
    @roles_required('admin')
    def post(self):
        args = section_parser.parse_args()
        this_section = Section.query.filter_by(name=args['name']).first()
        if this_section:
            raise HTTPStatus(409, 'Section already exists')
        new_section = Section(name=args['name'], description=args['description'])
        db.session.add(new_section)
        db.session.commit()
        raise HTTPStatus(201, 'Section created successfully')
    
    @auth_required('token')
    @roles_required('admin')
    def delete(self, section_id):
        this_section = Section.query.filter_by(id=section_id).first()
        if this_section:
            db.session.delete(this_section)
            db.session.commit()
            raise HTTPStatus(200, 'Section deleted successfully')
        else:
            raise HTTPStatus(404, 'Section not found')

    @auth_required('token')
    @roles_required('admin')
    def put(self, section_id):
        this_section = Section.query.filter_by(id=section_id).first()
        if this_section:
            args = section_parser.parse_args()
            this_section.name = args['name']
            this_section.description = args['description']
            db.session.commit()
            raise HTTPStatus(200, 'Section updated successfully')
        else:
            raise HTTPStatus(404, 'Section not found')

        
Associationsfields = {
    'user_id': fields.Integer,
    'ebook_id': fields.Integer,
    'date_issued': fields.DateTime,
    'date_return': fields.DateTime,
    'request_status': fields.String,
    'rating': fields.Integer,
    'user_email': fields.String,
    'ebook_name': fields.String,
    'ebook_authors': fields.String,
    'section_name': fields.String
}


class UserEbookApi(Resource):
    @auth_required('token')
    @marshal_with(Associationsfields)
    def get(self, user_id=None):
        if user_id:
            this_associations = UserEbookAssociation.query.filter_by(user_id=user_id).all()
            if this_associations:
                return this_associations, 200
            else:
                raise HTTPStatus(404, 'No associations found')
        this_associations = UserEbookAssociation.query.all()
        if this_associations:
            return this_associations, 200
        else:
            raise HTTPStatus(404, 'No associations found')
        
    @auth_required('token')
    @roles_required('admin')
    def delete(self, user_id):
        this_associations = UserEbookAssociation.query.filter_by(user_id=user_id).all()
        if this_associations:
            for user_ebook in this_associations:
                db.session.delete(user_ebook)
            db.session.commit()
            raise HTTPStatus(200, 'User ebooks deleted successfully')
        else:
            raise HTTPStatus(404, 'No user ebooks found')
        

Userfields = {
    'id': fields.Integer,
    'email': fields.String,
    'ebooks_requested': fields.Integer,
    'ebooks_issued': fields.Integer,
    'ebooks_purchased': fields.Integer
}

class UserApi(Resource):
    @auth_required('token')
    @marshal_with(Userfields)
    def get(self, user_id=None):
        if user_id:
            this_user = User.query.filter_by(id=user_id).first()
            if this_user:
                return this_user, 200
            else:
                raise HTTPStatus(404, 'User not found')
        else:
            all_users = User.query.all()
            if all_users:
                return all_users, 200
            else:
                raise HTTPStatus(404, 'No users found')
        

api.add_resource(EbookApi, '/ebooks', '/ebooks/<int:ebook_id>')
api.add_resource(SectionApi, '/sections', '/sections/<int:section_id>')
api.add_resource(UserEbookApi, '/associations', '/associations/<int:user_id>')
api.add_resource(UserApi, '/users', '/users/<int:user_id>')