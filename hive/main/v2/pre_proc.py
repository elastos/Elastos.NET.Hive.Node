from flask import request

from hive.main.v2 import view_auth
from hive.util.constants import APP_ID, DID
from hive.util.error_code import BAD_REQUEST, UNAUTHORIZED, SUCCESS
from hive.util.payment.vault_service_manage import can_access_vault, can_access_backup

def did_auth():
    info, err = view_auth.h_auth.get_token_info()
    if info:
        if APP_ID in info:
            return info[DID], info[APP_ID]
        else:
            return info[DID], None
    else:
        return None, None



def pre_proc(response, access_vault=None):
    did, app_id = did_auth()
    if (did is None) or (app_id is None):
        return did, app_id, response.response_err(UNAUTHORIZED, "auth failed")

    if access_vault:
        r, msg = can_access_vault(did, access_vault)
        if r != SUCCESS:
            return did, app_id, response.response_err(r, msg)

    return did, app_id, None


def post_json_param_pre_proc(response, *args, access_vault=None):
    did, app_id = did_auth()
    if (did is None) or (app_id is None):
        return did, app_id, None, response.response_err(UNAUTHORIZED, "auth failed")

    if access_vault:
        r, msg = can_access_vault(did, access_vault)
        if r != SUCCESS:
            return did, app_id, None, response.response_err(r, msg)

    content = request.get_json(force=True, silent=True)
    if content is None:
        return did, app_id, None, response.response_err(BAD_REQUEST, "parameter is not application/json")

    for arg in args:
        data = content.get(arg, None)
        if data is None:
            return did, app_id, None, response.response_err(BAD_REQUEST, "parameter " + arg + " is null")

    return did, app_id, content, None


def get_pre_proc(response, *args, access_vault=None):
    did, app_id = did_auth()
    if (did is None) or (app_id is None):
        return did, app_id, None, response.response_err(UNAUTHORIZED, "auth failed")

    if access_vault:
        r, msg = can_access_vault(did, access_vault)
        if r != SUCCESS:
            return did, app_id, None, response.response_err(r, msg)

    content = dict()
    for arg in args:
        data = request.args.get(arg, None)
        if data is None:
            return did, app_id, None, response.response_err(BAD_REQUEST, "parameter " + arg + " is null")
        else:
            content[arg] = data

    return did, app_id, content, None


def did_post_json_param_pre_proc(response, *args, access_vault=None, access_backup=None):
    did, app_id = did_auth()
    if did is None:
        return did, None, response.response_err(UNAUTHORIZED, "auth failed")

    content = request.get_json(force=True, silent=True)
    if content is None:
        return did, None, response.response_err(BAD_REQUEST, "parameter is not application/json")

    if access_vault:
        r, msg = can_access_vault(did, access_vault)
        if r != SUCCESS:
            return did, app_id, None, response.response_err(r, msg)

    if access_backup:
        r, msg = can_access_backup(did)
        if r != SUCCESS:
            return did, None, response.response_err(r, msg)

    for arg in args:
        data = content.get(arg, None)
        if data is None:
            return did, None, response.response_err(BAD_REQUEST, "parameter " + arg + " is null")

    return did, content, None


def did_get_param_pre_proc(response, *args, access_vault=None, access_backup=None):
    did, app_id = did_auth()
    if did is None:
        return did, None, response.response_err(UNAUTHORIZED, "auth failed")

    if access_vault:
        r, msg = can_access_vault(did, access_vault)
        if r != SUCCESS:
            return did, app_id, None, response.response_err(r, msg)

    if access_backup:
        r, msg = can_access_backup(did)
        if r != SUCCESS:
            return did, None, response.response_err(r, msg)

    content = dict()
    for arg in args:
        data = request.args.get(arg, None)
        if data is None:
            return did, app_id, None, response.response_err(BAD_REQUEST, "parameter " + arg + " is null")
        else:
            content[arg] = data
    return did, content, None
