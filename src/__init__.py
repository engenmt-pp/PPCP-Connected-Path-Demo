#!/usr/bin/env python3

import os
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")
    app.jinja_env.globals.update(
        zip=zip
    )  # Allows for the use of `zip` in Jinja2 formatting.

    os.makedirs(app.instance_path, exist_ok=True)

    from . import api, partner, store, reports
    from . import store_merchant

    app.register_blueprint(api.bp)
    app.register_blueprint(reports.bp)

    app.register_blueprint(partner.bp)
    app.register_blueprint(store.bp)
    app.add_url_rule("/", endpoint="store.checkout_capture")

    app.register_blueprint(store_merchant.bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
