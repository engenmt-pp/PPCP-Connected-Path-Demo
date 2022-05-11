import json

# import secrets

from flask import Blueprint, render_template
from .api import (
    generate_onboarding_urls,
    get_merchant_id,
    get_onboarding_status,
    get_referral_status,
    get_partner_referral_id,
)

bp = Blueprint("lipp", __name__, url_prefix="/lipp")


@bp.route("/")
def login_with_paypal():
    return render_template("lipp.html")
