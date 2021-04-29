import json
from datetime import datetime

from bson import json_util

from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

from hive.settings import hive_setting
from hive.util.constants import VAULT_ACCESS_WR, VAULT_ACCESS_R, VAULT_ACCESS_DEL
from hive.util.did_mongo_db_resource import gene_mongo_db_name, options_filter, gene_sort, convert_oid, \
    populate_options_find_many, query_insert_one, query_find_many, populate_options_insert_one, query_count_documents, \
    populate_options_count_documents, query_update_one, populate_options_update_one, query_delete_one, get_collection, \
    get_mongo_database_size
from hive.util.error_code import INTERNAL_SERVER_ERROR, BAD_REQUEST, NOT_FOUND
from hive.util.server_response import ServerResponseV2
from hive.main.interceptor import post_json_param_pre_proc
from hive.util.payment.vault_service_manage import update_vault_db_use_storage_byte


class HiveMongoDb:
    def __init__(self, app=None):
        self.app = app
        self.response = ServerResponseV2("HiveMongoDb")

    def init_app(self, app):
        self.app = app

    def create_collection(self, did, app_id, collection):
        if hive_setting.MONGO_URI:
            uri = hive_setting.MONGO_URI
            connection = MongoClient(uri)
        else:
            connection = MongoClient(host=hive_setting.MONGO_HOST, port=hive_setting.MONGO_PORT)

        db_name = gene_mongo_db_name(did, app_id)
        db = connection[db_name]
        try:
            col = db.create_collection(collection)
        except CollectionInvalid:
            return self.response.response_ok()
        except Exception as e:
            return self.response.response_err(INTERNAL_SERVER_ERROR, "Exception:" + str(e))
        return self.response.response_ok(status_code=201)

    def delete_collection(self, did, app_id, collection):
        if hive_setting.MONGO_URI:
            uri = hive_setting.MONGO_URI
            connection = MongoClient(uri)
        else:
            connection = MongoClient(host=hive_setting.MONGO_HOST, port=hive_setting.MONGO_PORT)

        db_name = gene_mongo_db_name(did, app_id)
        db = connection[db_name]
        try:
            db.drop_collection(collection)
            db_size = get_mongo_database_size(did, app_id)
            update_vault_db_use_storage_byte(did, db_size)
        except CollectionInvalid:
            pass
        except Exception as e:
            return self.response.response_err(INTERNAL_SERVER_ERROR, "Exception:" + str(e))
        return self.response.response_ok(status_code=204)

    def insert_many(self, did, app_id, collection, content):
        col = get_collection(did, app_id, collection)
        if not col:
            return self.response.response_err(NOT_FOUND, "collection not exist")

        options = options_filter(content, ("bypass_document_validation", "ordered"))

        try:
            new_document = []
            for document in content["document"]:
                document["created"] = datetime.utcnow()
                document["modified"] = datetime.utcnow()
                new_document.append(convert_oid(document))

            ret = col.insert_many(new_document, **options)
            db_size = get_mongo_database_size(did, app_id)
            update_vault_db_use_storage_byte(did, db_size)
            data = {
                "acknowledged": ret.acknowledged,
                "inserted_ids": [str(_id) for _id in ret.inserted_ids]
            }
            return self.response.response_ok(data, status_code=201)
        except Exception as e:
            return self.response.response_err(INTERNAL_SERVER_ERROR, "Exception:" + str(e))

    def update_many(self, did, app_id, collection, content):
        col = get_collection(did, app_id, collection)
        if not col:
            return self.response.response_err(NOT_FOUND, "collection not exist")

        options = options_filter(content, ("upsert", "bypass_document_validation"))

        try:
            update_set_on_insert = content.get('update').get('$setOnInsert', None)
            if update_set_on_insert:
                content["update"]["$setOnInsert"]['created'] = datetime.utcnow()
            else:
                content["update"]["$setOnInsert"] = {
                    "created": datetime.utcnow()
                }
            if "$set" in content["update"]:
                content["update"]["$set"]["modified"] = datetime.utcnow()
            ret = col.update_many(convert_oid(content["filter"]), convert_oid(content["update"], update=True),
                                  **options)
            data = {
                "acknowledged": ret.acknowledged,
                "matched_count": ret.matched_count,
                "modified_count": ret.modified_count,
                "upserted_id": str(ret.upserted_id)
            }
            db_size = get_mongo_database_size(did, app_id)
            update_vault_db_use_storage_byte(did, db_size)
            return self.response.response_ok(data)
        except Exception as e:
            return self.response.response_err(INTERNAL_SERVER_ERROR, "Exception:" + str(e))

    def delete_many(self, did, app_id, collection, content):
        col = get_collection(did, app_id, collection)
        if not col:
            return self.response.response_err(NOT_FOUND, "collection not exist")

        try:
            ret = col.delete_many(convert_oid(content["filter"]))
            data = {
                "acknowledged": ret.acknowledged,
                "deleted_count": ret.deleted_count,
            }
            db_size = get_mongo_database_size(did, app_id)
            update_vault_db_use_storage_byte(did, db_size)
            return self.response.response_ok(data, status_code=204)
        except Exception as e:
            return self.response.response_err(INTERNAL_SERVER_ERROR, "Exception:" + str(e))

    def count_documents(self, did, app_id, collection, content):
        options = populate_options_count_documents(content)

        col = get_collection(did, app_id, collection)
        if not col:
            return self.response.response_err(NOT_FOUND, "collection not exist")

        data, err_message = query_count_documents(col, content, options)
        if err_message:
            return self.response.response_err(INTERNAL_SERVER_ERROR, err_message)

        return self.response.response_ok(data)

    def find_many(self, did, app_id, collection, content):
        options = populate_options_find_many(content)

        col = get_collection(did, app_id, collection)
        if not col:
            return self.response.response_err(NOT_FOUND, "collection not exist")

        data, err_message = query_find_many(col, content, options)
        if err_message:
            return self.response.response_err(INTERNAL_SERVER_ERROR, err_message)

        return self.response.response_ok(data)
