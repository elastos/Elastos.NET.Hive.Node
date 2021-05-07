import json

from flask import Blueprint, request
from urllib.parse import quote, unquote
from hive.main.v2.hive_mongo import HiveMongoDb
from hive.main.v2.pre_proc import pre_proc, post_json_param_pre_proc
from hive.util.constants import VAULT_ACCESS_WR, VAULT_ACCESS_DEL, VAULT_ACCESS_R
from hive.util.error_code import BAD_REQUEST

h_mongo_db = HiveMongoDb()

hive_db = Blueprint('hive_db_v2', __name__)


def init_app(app):
    h_mongo_db.init_app(app)
    app.register_blueprint(hive_db)


@hive_db.route('/api/v2/vault/db/<path:collection>', methods=['PUT'])
def view_create_collection(collection):
    did, app_id, response = pre_proc(h_mongo_db.response, access_vault=VAULT_ACCESS_WR)
    if response is not None:
        return response

    return h_mongo_db.create_collection(did, app_id, collection)


@hive_db.route('/api/v2/vault/db/<path:collection>', methods=['DELETE'])
def view_delete_collection(collection):
    did, app_id, response = pre_proc(h_mongo_db.response, access_vault=VAULT_ACCESS_WR)
    if response is not None:
        return response
    return h_mongo_db.delete_collection(did, app_id, collection)


@hive_db.route('/api/v2/vault/db/collection/<path:collection>', methods=['POST'])
def view_insert_many(collection):
    did, app_id, content, err = post_json_param_pre_proc(h_mongo_db.response, "document",
                                                         access_vault=VAULT_ACCESS_WR)
    if err:
        return err
    return h_mongo_db.insert_many(did, app_id, collection, content)


@hive_db.route('/api/v2/vault/db/collection/<path:collection>', methods=['PATCH'])
def view_update_many(collection):
    did, app_id, content, err = post_json_param_pre_proc(h_mongo_db.response, "filter", "update",
                                                         access_vault=VAULT_ACCESS_WR)
    if err:
        return err
    return h_mongo_db.update_many(did, app_id, collection, content)


@hive_db.route('/api/v2/vault/db/collection/<path:collection>', methods=['DELETE'])
def view_delete_many(collection):
    did, app_id, content, err = post_json_param_pre_proc(h_mongo_db.response, "filter",
                                                         access_vault=VAULT_ACCESS_DEL)
    if err:
        return err
    return h_mongo_db.delete_many(did, app_id, collection, content)


@hive_db.route('/api/v2/vault/db/collection/<path:collection>', methods=['GET'])
def view_get_documents_info(collection):
    did, app_id, response = pre_proc(h_mongo_db.response, access_vault=VAULT_ACCESS_R)
    if response is not None:
        return response

    content = dict()
    try:
        fi_str = unquote(request.args.get('filter', '', type=str))
        if fi_str:
            fi = json.loads(fi_str)
        else:
            fi = dict()
        skip = request.args.get('skip', -1, type=int)
        limit = request.args.get('limit', -1, type=int)
    except Exception as e:
        return h_mongo_db.response.response_err(BAD_REQUEST, f"Exception: {str(e)}")
    if fi:
        content["filter"] = fi
    op = dict()
    if skip != -1:
        op['skip'] = skip
    if limit != -1:
        op['limit'] = limit
    if op:
        content["options"] = op

    count = request.args.get('count')
    if count is None:
        return h_mongo_db.find_many(did, app_id, collection, content)
    else:
        return h_mongo_db.count_documents(did, app_id, collection, content)


@hive_db.route('/api/v2/vault/db/collection/<path:collection>/query', methods=['POST'])
def view_find(collection):
    did, app_id, content, err = post_json_param_pre_proc(h_mongo_db.response, access_vault=VAULT_ACCESS_R)
    if err:
        return err
    return h_mongo_db.find_many(did, app_id, collection, content)
