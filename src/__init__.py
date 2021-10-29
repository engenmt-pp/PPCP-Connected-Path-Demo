import os
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    os.makedirs(app.instance_path, exist_ok=True)

    from . import api, partner, store

    app.register_blueprint(api.bp)
    app.register_blueprint(partner.bp)

    app.register_blueprint(store.bp)
    app.add_url_rule("/", endpoint="store.checkout")

    return app