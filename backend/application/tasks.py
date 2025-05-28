from celery import shared_task
from datetime import datetime, timedelta
import flask_excel as excel
from .models import *
from .mail_service import send_email
from jinja2 import Template


@shared_task()
def create_csv():
    associations = UserEbookAssociation.query.filter_by(
        request_status='issued').all()
    if not associations:
        return 'No data found'
    data = [
        [association.user.email, association.ebook.name, association.section_name, association.ebook.authors, association.rating, association.date_issued.strftime("%B %d, %Y"), association.date_return.strftime("%B %d, %Y")] for association in associations
    ]
    csv_out = excel.make_response_from_query_sets(
        data, ['email', 'ebook_name', 'section', 'authors', 'rating by user', 'date_issued', 'date_return'], 'csv', file_name='data.csv')

    with open('./user_downloads/data.csv', 'wb') as file:
        file.write(csv_out.data)
    return 'csv created'

@shared_task
def create_pdf(ebook_id):
    ebook = Ebook.query.filter_by(id=ebook_id).first()

    if not ebook:
        return 'Ebook not found'

    with open(f'./user_downloads/{ebook.name}.pdf', 'w') as file:
        file.write(ebook.content)
    return f'{ebook.name}.pdf'

@shared_task()
def send_return_date_reminder():
    # Query all UserEbookAssociations where the return date is approaching
    associations = UserEbookAssociation.query.filter(
        UserEbookAssociation.request_status == 'issued',
        UserEbookAssociation.date_return <= datetime.now() + timedelta(days=2)
    )

    for association in associations:
        date_return = association.date_return.strftime("%B %d, %Y")
        # Send an email to the user
        send_email(
            to=association.user.email,
            subject="Return date approaching for eBook",
            content_body=f"Dear {association.user.email}, your return date for eBook '{association.ebook.name}' is approaching. Your access will be revoked on {date_return}. Thank you for using our service.",
        )

    return "OK"


@shared_task()
def revoke_expired_access():
    associations = UserEbookAssociation.query.filter(
        UserEbookAssociation.request_status == 'issued',
        UserEbookAssociation.date_return < datetime.now()
    )

    for association in associations:
        association.request_status = 'revoked'
        association.date_issued = None
        association.date_return = None

        # Send an email to the user
        send_email(
            to=association.user.email,
            subject="EBook access revoked",
            content_body=f"Dear {association.user.email}, your access to eBook '{association.ebook.name}' has been revoked. Thank you for using our service.",
        )

    db.session.commit()
    return "OK"

@shared_task()
def monthly_report():
    ebooks = Ebook.query.all()
    issued = UserEbookAssociation.query.filter_by(request_status='issued').all()
    
    # geting the most issued ebook
    most_issued = sorted(ebooks, key=lambda x: len(UserEbookAssociation.query.filter_by(ebook_id=x.id, request_status='issued').all()), reverse=True)[0]
    no_of_users = len(UserEbookAssociation.query.filter_by(ebook_id=most_issued.id, request_status='issued').all())
    # geting the highest rated ebook
    highest_rated = sorted(ebooks, key=lambda x: x.average_rating if x.average_rating is not None else 0, reverse=True)[0]
    # Generate HTML report
    html_template = """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Monthly Report</h1>
        {% if most_issued %}
        <h3>Most issued ebook </h3>
            <p>Name: {{ most_issued.name }}</p>
            <p>Authors: {{ most_issued.authors }}</p>
            <p>Section: {{ most_issued.section_name }}</p>
            <p>Number of users: {{ no_of_users }}</p>
        {% endif %}
        {% if highest_rated %}
        <h3>Highest rated ebook </h3>
            <p>Name: {{ highest_rated.name }}</p>
            <p>Authors: {{ highest_rated.authors }}</p>
            <p>Section: {{ highest_rated.section_name }}</p>
            <p>Average rating: {{ highest_rated.average_rating }}</p>
        {% endif %}
        <h3>Issued books </h3>
            <ul>
                {% for association in issued %}
                    <li>
                        Name: {{ association.ebook.name }} <br>
                        Section: {{ association.section_name }} <br>
                        Issued_to: {{ association.user.email }} <br>
                        Rating: {{ association.rating }} <br>
                        Date issued: {{ association.date_issued.strftime("%B %d, %Y") }} <br>
                        Date returned: {{ association.date_return.strftime("%B %d, %Y") }} <br>
                    </li>
                {% endfor %}
            </ul>

    </body>
    </html>
"""

    template = Template(html_template)
    report_html = template.render(issued=issued, most_issued=most_issued, no_of_users=no_of_users, highest_rated=highest_rated)

    send_email(
        to= 'admin@abc.in',
        subject="Monthly Report",
        content_body=report_html
    )
    return "OK"