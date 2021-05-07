import logging
from datetime import datetime
import traceback
from hive.util.error_code import INTERNAL_SERVER_ERROR
from hive.util.server_response_v2 import ServerResponseV2

def init_app(app):
    app.register_error_handler(INTERNAL_SERVER_ERROR, handle_exception_500)


def handle_exception_500(e):
    response = ServerResponseV2("HiveNode")
    logging.getLogger("Hive exception").exception(f"handle_exception_500: {traceback.format_exc()}")
    return response.response_err(INTERNAL_SERVER_ERROR, f"Exception at {str(datetime.utcnow())} error is:{str(e)}")
