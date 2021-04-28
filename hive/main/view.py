from flask import Blueprint, request, jsonify, Response

from hive.main.hive_manage import HiveManage

h_manage = HiveManage()

main = Blueprint('main', __name__)


def init_app(app):
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


