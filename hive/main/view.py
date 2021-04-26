from flask import Blueprint, request, jsonify, Response

from hive.main.hive_auth import HiveAuth
from hive.main.hive_manage import HiveManage

h_auth = HiveAuth()
h_manage = HiveManage()

main = Blueprint('main', __name__)


def init_app(app):
    h_auth.init_app(app)
    h_manage.init_app(app)
    app.register_blueprint(main)


@main.route('/api/v2/echo', defaults={'file_name':None}, methods=['POST', 'PUT', 'GET', 'PATCH', 'DELETE'])
@main.route('/api/v2/echo/<path:file_name>', methods=['POST', 'PUT', 'GET', 'PATCH', 'DELETE'])
def echo(file_name):
    if request.method == 'GET':
        var = request.args
        content = var
        return jsonify(content)
    else:
        content = request.get_json()
        if content:
            return jsonify(content)
        else:
            resp = Response()
            resp.status_code = 200
            return resp


# hive version
@main.route('/api/v2/hive/version', methods=['GET'])
def get_hive_version():
    return h_manage.get_hive_version()


# hive commit hash
@main.route('/api/v2/hive/commithash', methods=['GET'])
def get_hive_commit_hash():
    return h_manage.get_hive_commit_hash()


# did auth
@main.route('/api/v2/did/sign_in', methods=['POST'])
def access_request():
    return h_auth.sign_in()


@main.route('/api/v2/did/auth', methods=['POST'])
def request_did_auth():
    return h_auth.request_did_auth()


@main.route('/api/v2/did/check_token', methods=['POST'])
def check_token():
    return h_auth.check_token()


@main.route('/api/v2/did/backup_auth', methods=['POST'])
def backup_auth():
    return h_auth.backup_auth()


@main.route('/api/v2/did/check_backup_token', methods=['POST'])
def check_backup_token():
    return h_auth.check_backup_token()


@main.route('/api/v2/did/<did_base58>/<app_id_base58>/callback', methods=['POST'])
def did_auth_callback(did_base58, app_id_base58):
    return h_auth.did_auth_callback(did_base58, app_id_base58)
