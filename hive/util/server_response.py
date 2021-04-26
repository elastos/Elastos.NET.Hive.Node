import json

from flask import jsonify, Response
import logging


class ServerResponseV2:
    def __init__(self, logger_name="HiveNode"):
        self.logger = logging.getLogger(logger_name)

    def response_ok(self, data_dic=None, status_code=200):
        if not data_dic:
            resp = Response()
            resp.status_code = status_code
            return resp
        else:
            self.logger.debug(json.dumps(data_dic))
            return jsonify(data_dic), status_code

    def response_err(self, status_code, msg, code=None):
        if code:
            ret = ({"error": {"code": code, "message": msg}})
        else:
            ret = ({"error": {"message": msg}})
        self.logger.error(msg)
        return jsonify(ret), status_code
