from flask import request, jsonify, send_file
from flask_security import auth_required, roles_required
from flask_security.utils import hash_password, verify_password
from datetime import datetime, timedelta
from .extensions import db, security
from .exceptions import HTTPStatus
from flask import current_app as app
from .models import *
from .tasks import create_csv, create_pdf
from celery.result import AsyncResult

user_datastore = security.datastore

@app.post('/api/login')
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        raise HTTPStatus(400, 'Invalid Input')
    
    user = user_datastore.find_user(email=email)

    if not user:
        raise HTTPStatus(401, 'User not found')

    if verify_password(password, user.password):
        data = {'email': email, 'id': user.id, 'role' : user.roles[0].name , 'token' : user.get_auth_token()}
        return jsonify(data)

    raise HTTPStatus(401, 'Wrong password')


@app.post('/api/signup')
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = 'user'

    if not email or not password:
        raise HTTPStatus(400, 'Invalid Input')
    
    if user_datastore.find_user(email=email):
        raise HTTPStatus(409, 'User already exists')

    try:
        user_datastore.create_user(
            email=email,
            password=hash_password(password),
            roles=[role],
            active=True
        )
        db.session.commit()
    except:
        db.session.rollback()
        raise HTTPStatus(500, 'Error while creating user')
    raise HTTPStatus(201, 'User created successfully')

@app.get('/api/request-ebook/<int:user_id>/<int:ebook_id>')
def request_ebook(user_id, ebook_id):
    user = user_datastore.find_user(id=user_id)
    ebook = Ebook.query.filter_by(id=ebook_id).first()

    if not user or not ebook:
        raise HTTPStatus(404, 'User or Ebook not found')

    if user.is_max_ebooks_limit():
        raise HTTPStatus(403, 'You have already requested the maximum number of ebooks (5).')

    this_association = UserEbookAssociation.query.filter_by(user_id=user_id, ebook_id=ebook_id).first()
    if this_association:
        this_association.request_status = 'requested'
        db.session.commit()
        raise HTTPStatus(200, 'Ebook requested successfully')

    new_association = UserEbookAssociation(user_id=user_id, ebook_id=ebook_id, request_status='requested')
    db.session.add(new_association)
    db.session.commit()
    raise HTTPStatus(201, 'Ebook requested successfully')

@app.get('/api/grant-request/<int:user_id>/<int:ebook_id>')
@auth_required('token')
@roles_required('admin')
def grant_request(user_id, ebook_id):

    this_association = UserEbookAssociation.query.filter_by(user_id=user_id, ebook_id=ebook_id).first()
    if this_association:
        this_association.request_status = 'issued'
        this_association.date_issued = datetime.utcnow()
        this_association.date_return = datetime.utcnow() + timedelta(days=this_association.ebook.acces_duration)
        db.session.commit()
        raise HTTPStatus(200, 'Request granted successfully')

    raise HTTPStatus(404, 'Request not found')


@app.get('/api/reject-request/<int:user_id>/<int:ebook_id>')
@auth_required('token')
@roles_required('admin')
def reject_request(user_id, ebook_id):

    this_association = UserEbookAssociation.query.filter_by(user_id=user_id, ebook_id=ebook_id).first()
    if this_association:
        this_association.request_status = 'rejected'
        db.session.commit()
        raise HTTPStatus(200, 'Request rejected successfully')

    raise HTTPStatus(404, 'Request not found')


@app.get('/api/revoke-access/<int:user_id>/<int:ebook_id>')
@auth_required('token')
@roles_required('admin')
def revoke_access(user_id, ebook_id):

    this_association = UserEbookAssociation.query.filter_by(user_id=user_id, ebook_id=ebook_id).first()
    if this_association:
        # this_association.date_return = datetime.utcnow()
        this_association.request_status = 'revoked'
        this_association.date_return = None
        this_association.date_issued = None
        db.session.commit()
        raise HTTPStatus(200, 'Access revoked successfully')

    raise HTTPStatus(404, 'Access not found')

@app.get('/api/return-ebook/<int:user_id>/<int:ebook_id>')
@auth_required('token')
def return_ebook(user_id, ebook_id):

    this_association = UserEbookAssociation.query.filter_by(user_id=user_id, ebook_id=ebook_id).first()
    if this_association:
        this_association.request_status = 'returned'
        this_association.date_return = None
        this_association.date_issued = None
        db.session.commit()
        raise HTTPStatus(200, 'Ebook returned successfully')

    raise HTTPStatus(404, 'Ebook not found')

@app.get('/api/buy-ebook/<int:user_id>/<int:ebook_id>')
@auth_required('token')
def buy_ebook(user_id, ebook_id):

    this_association = UserEbookAssociation.query.filter_by(user_id=user_id, ebook_id=ebook_id).first()
    if this_association:
        this_association.request_status = 'purchased'
        this_association.date_issued = None
        this_association.date_return = None
        db.session.commit()
        raise HTTPStatus(200, 'Ebook purchased successfully')

    raise HTTPStatus(404, 'Ebook not found')

@app.post('/api/rate-ebook/<int:user_id>/<int:ebook_id>')
@auth_required('token')
def rate_ebook(user_id, ebook_id):

    this_association = UserEbookAssociation.query.filter_by(user_id=user_id, ebook_id=ebook_id).first()
    if this_association:
        data = request.get_json()
        this_association.rating = data.get('rating')
        db.session.commit()
        raise HTTPStatus(200, 'Ebook rated successfully')

    raise HTTPStatus(404, 'Ebook not found')

@app.get('/api/user-stats/<int:user_id>')
@auth_required('token')
def user_stats(user_id):
    # total ebooks in library
    total_ebooks = len(Ebook.query.all())
    # total issued ebooks
    total_issued = len(UserEbookAssociation.query.filter_by(user_id=user_id, request_status='issued').all())
    # total purchased ebooks
    total_purchased = len(UserEbookAssociation.query.filter_by(user_id=user_id, request_status='purchased').all())
    # total requested ebooks
    total_requested = len(UserEbookAssociation.query.filter_by(user_id=user_id, request_status='requested').all())
    
    data = {
        'total_ebooks': total_ebooks,
        'total_issued': total_issued,
        'total_purchased': total_purchased,
        'total_requested': total_requested
    }
    
    return data

@app.get('/api/admin-stats')
@auth_required('token')
@roles_required('admin')
def admin_stats():
    # total ebooks in library
    total_ebooks = len(Ebook.query.all())
    # total users
    total_users = len(User.query.all())
    data = {
        'total_ebooks': total_ebooks,
        'total_users': total_users
    }
    return data

@app.route('/get-task/<task_id>')
@auth_required('token')
@roles_required('admin')
def get_task(task_id):
    result = AsyncResult(task_id)
    if result.ready():
        return jsonify({'result': result.result}), 200
    else:
        raise HTTPStatus(405, 'Task not ready')
    
@app.route('/start-export')
@auth_required('token')
@roles_required('admin')
def start_export():
    task = create_csv.delay()
    return jsonify({'task_id': task.id})
    
@app.route('/create-pdf/<ebook_id>')
@auth_required('token')
def start_pdf(ebook_id):
    task = create_pdf.delay(ebook_id)
    return jsonify({'task_id': task.id})

@app.route('/download-pdf/<task_id>')
@auth_required('token')
def get_pdf(task_id):
    result = AsyncResult(task_id)
    if result.ready():
        return send_file(f'./user_downloads/{result.result}', mimetype='application/pdf', as_attachment=True), 200
    else:
        raise HTTPStatus(405, 'Task not ready')