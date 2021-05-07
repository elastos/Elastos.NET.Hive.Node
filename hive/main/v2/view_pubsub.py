from flask import Blueprint
from hive.main.v2.hive_pubsub import HivePubSub

h_pubsub = HivePubSub()
hive_pubsub = Blueprint('hive_pubsub_v2', __name__)


def init_app(app, mode):
    h_pubsub.init_app(app)
    app.register_blueprint(hive_pubsub)


@hive_pubsub.route('/api/v2/pubsub/publish', methods=['POST'])
def pb_publish_channel():
    return h_pubsub.publish_channel()


@hive_pubsub.route('/api/v2/pubsub/remove', methods=['POST'])
def pb_remove_channel():
    return h_pubsub.remove_channel()


@hive_pubsub.route('/api/v2/pubsub/pub/channels', methods=['GET'])
def pb_get_publish_channels():
    return h_pubsub.get_pub_channels()


@hive_pubsub.route('/api/v2/pubsub/sub/channels', methods=['GET'])
def pb_get_subscribe_channels():
    return h_pubsub.get_sub_channels()


@hive_pubsub.route('/api/v2/pubsub/subscribe', methods=['POST'])
def pb_subscribe_channel():
    return h_pubsub.subscribe_channel()


@hive_pubsub.route('/api/v2/pubsub/unsubscribe', methods=['POST'])
def pb_unsubscribe_channel():
    return h_pubsub.unsubscribe_channel()


@hive_pubsub.route('/api/v2/pubsub/push', methods=['POST'])
def pb_push_message():
    return h_pubsub.push_message()


@hive_pubsub.route('/api/v2/pubsub/pop', methods=['POST'])
def pb_pop_messages():
    return h_pubsub.pop_messages()