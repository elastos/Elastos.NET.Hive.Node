from flask import Blueprint, request, jsonify, Response

from hive.main.hive_auth import HiveAuth
from hive.util.error_code import BAD_REQUEST

h_auth = HiveAuth()
auth = Blueprint('auth', __name__)


def init_app(app):
    h_auth.init_app(app)
    app.register_blueprint(auth)


# did auth
@auth.route('/api/v2/did/signin', methods=['POST'])
def access_request():
    body = request.get_json(force=True, silent=True)
    if body is None:
        return h_auth.response.response_err(BAD_REQUEST, "parameter is not application/json")
    document = body.get('id', None)
    if document is None:
        return h_auth.response.response_err(BAD_REQUEST, "The parameter is null")

    return h_auth.sign_in(document)


@auth.route('/api/v2/did/auth', methods=['POST'])
def request_did_auth():
    return h_auth.request_did_auth()


@auth.route('/api/v2/did/check_token', methods=['POST'])
def check_token():
    return h_auth.check_token()


@auth.route('/api/v2/did/backup_auth', methods=['POST'])
def backup_auth():
    return h_auth.backup_auth()
