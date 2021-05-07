from . import view, view_auth, view_db, view_file, view_scripting, view_payment, pre_proc, view_internal, \
    view_backup, view_pubsub


def init_app(app, mode):
    view.init_app(app)
    view_auth.init_app(app)
    view_db.init_app(app)
    view_file.init_app(app)
    view_scripting.init_app(app)
    view_payment.init_app(app)
    view_internal.init_app(app, mode)
    view_backup.init_app(app, mode)
    view_pubsub.init_app(app, mode)
