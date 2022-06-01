from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix="/api")

from . import orders, referrals

bp.register_blueprint(orders.bp)
bp.register_blueprint(referrals.bp)
