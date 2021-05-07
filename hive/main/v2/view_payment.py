from flask import Blueprint

from hive.main.v2.hive_payment import HivePayment

h_payment = HivePayment()
hive_payment = Blueprint('hive_payment_v2', __name__)


def init_app(app):
    h_payment.init_app(app)
    app.register_blueprint(hive_payment)


@hive_payment.route('/api/v2/payment/version', methods=['GET'])
def get_version():
    return h_payment.get_version()


@hive_payment.route('/api/v2/payment/vault_package_info', methods=['GET'])
def get_vault_package_info():
    return h_payment.get_vault_package_info()


@hive_payment.route('/api/v2/payment/vault_pricing_plan', methods=['GET'])
def get_vault_pricing_plan():
    return h_payment.get_vault_pricing_plan()


@hive_payment.route('/api/v2/payment/create_vault_package_order', methods=['POST'])
def create_vault_package_order():
    return h_payment.create_vault_package_order()


@hive_payment.route('/api/v2/payment/pay_vault_package_order', methods=['POST'])
def pay_vault_package_order():
    return h_payment.pay_vault_package_order()


@hive_payment.route('/api/v2/payment/cancel_vault_package_order', methods=['POST'])
def cancel_vault_package_order():
    return h_payment.cancel_vault_package_order()


@hive_payment.route('/api/v2/payment/vault_package_order', methods=['GET'])
def vault_package_order():
    return h_payment.get_vault_package_order()


@hive_payment.route('/api/v2/payment/vault_package_order_list', methods=['GET'])
def vault_package_order_list():
    return h_payment.get_vault_package_order_list()


@hive_payment.route('/api/v2/payment/vault_backup_plan', methods=['GET'])
def get_vault_backup_plan():
    return h_payment.get_vault_backup_plan()


# ------------------------------------ service ------------------------------------

@hive_payment.route('/api/v2/service/vault/create', methods=['POST'])
def create_vault():
    return h_payment.create_free_vault()


@hive_payment.route('/api/v2/service/vault/remove', methods=['POST'])
def remove_vault():
    return h_payment.remove_vault()


@hive_payment.route('/api/v2/service/vault/freeze', methods=['POST'])
def freeze_vault():
    return h_payment.freeze_vault()


@hive_payment.route('/api/v2/service/vault/unfreeze', methods=['POST'])
def unfreeze_vault():
    return h_payment.unfreeze_vault()


@hive_payment.route('/api/v2/service/vault', methods=['GET'])
def get_vault_service_info():
    return h_payment.get_vault_service_info()


@hive_payment.route('/api/v2/service/vault_backup/create', methods=['POST'])
def create_free_vault_backup():
    return h_payment.create_free_vault_backup()


@hive_payment.route('/api/v2/service/vault_backup', methods=['GET'])
def get_vault_backup_service_info():
    return h_payment.get_vault_backup_service_info()
