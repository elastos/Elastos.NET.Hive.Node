import sentry_sdk
import logging

from hive.util.constants import HIVE_MODE_DEV, HIVE_MODE_TEST
from . import scheduler, v1, v2, interceptor
from ..settings import hive_setting
from sentry_sdk.integrations.flask import FlaskIntegration

logging.getLogger().level = logging.INFO


def init_app(app, mode):
    logging.getLogger("Hive").info("##############################")
    logging.getLogger("Hive").info("HIVE BACK-END IS STARTING")
    logging.getLogger("Hive").info("##############################")

    if mode != HIVE_MODE_TEST and hive_setting.HIVE_SENTRY_DSN != "":
        sentry_sdk.init(
            dsn=hive_setting.HIVE_SENTRY_DSN,
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0
        )

    interceptor.init_app(app)
    v2.init_app(app, mode)
    v1.init_app(app, mode)
    if mode == HIVE_MODE_TEST:
        scheduler.scheduler_init(app, paused=True)
    else:
        scheduler.scheduler_init(app, paused=False)
