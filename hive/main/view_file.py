from flask import Blueprint, request

from hive.main.hive_file import HiveFile
from hive.main.interceptor import get_pre_proc, pre_proc
from hive.util.constants import VAULT_ACCESS_WR, VAULT_ACCESS_R, VAULT_ACCESS_DEL
from hive.util.error_code import NOT_ACCEPTABLE, FORBIDDEN

h_file = HiveFile()

hive_file = Blueprint('hive_file', __name__)


def init_app(app):
    h_file.init_app(app)
    app.register_blueprint(hive_file)


@hive_file.route('/api/v2/vault/files/<path:file_name>', methods=['PUT'])
def upload_file(file_name):
    did, app_id, response = pre_proc(h_file.response, access_vault=VAULT_ACCESS_WR)
    if response is not None:
        return response
    return h_file.upload_file(did, app_id, file_name)


@hive_file.route('/api/v2/vault/files', defaults={'file_name': '/'}, methods=['GET'])
@hive_file.route('/api/v2/vault/files/<path:file_name>', methods=['GET'])
def get_file(file_name):
    did, app_id, response = pre_proc(h_file.response, access_vault=VAULT_ACCESS_R)
    if response is not None:
        return response

    op = request.args.get('comp')
    if op is None:
        if file_name:
            return h_file.download_file(did, app_id, file_name)
        else:
            return h_file.response.response_err(FORBIDDEN, "Can not download directory")
    elif op == "metadata":
        return h_file.get_property(did, app_id, file_name)
    elif op == "children":
        return h_file.list_files(did, app_id, file_name)
    elif op == "hash":
        return h_file.file_hash(did, app_id, file_name)


@hive_file.route('/api/v2/vault/files', defaults={'file_name': None}, methods=['DELETE'])
@hive_file.route('/api/v2/vault/files/<path:file_name>', methods=['DELETE'])
def remove(file_name):
    did, app_id, response = pre_proc(h_file.response, access_vault=VAULT_ACCESS_DEL)
    if response is not None:
        return response
    return h_file.delete(did, app_id, file_name)


@hive_file.route('/api/v2/vault/files/<path:src_name>', methods=['PATCH'])
def move_files(src_name):
    did, app_id, content, response = get_pre_proc(h_file.response, "to", access_vault=VAULT_ACCESS_WR)
    if response is not None:
        return response
    dst_name = content["to"]
    return h_file.move(did, app_id, src_name, dst_name, is_copy=False)


@hive_file.route('/api/v2/vault/files/<path:src_name>', methods=['POST'])
def copy_files(src_name):
    did, app_id, content, response = get_pre_proc(h_file.response, "dst", access_vault=VAULT_ACCESS_WR)
    if response is not None:
        return response
    dst_name = content["dst"]
    return h_file.move(did, app_id, src_name, dst_name, is_copy=True)
