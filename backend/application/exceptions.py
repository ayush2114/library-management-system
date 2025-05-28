from werkzeug.exceptions import HTTPException
from flask import make_response
import json


class HTTPStatus(HTTPException):
    def __init__(self, status_code, message):
        message = {"message": message}
        self.response = make_response(json.dumps(message), status_code)
