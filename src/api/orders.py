import json
from flask import Blueprint, jsonify, request
from .utils import build_endpoint, build_headers, log_and_request

bp = Blueprint("orders", __name__, url_prefix="/orders")


@bp.route("/create", methods=("POST",))
def create_for_capture(include_platform_fees=True):
    """Create an order with "intent: CAPTURE" with the /v2/checkout/orders API.

    Requires `price` and `payee_id` fields in the request body.

    Docs: https://developer.paypal.com/docs/api/orders/v2/#orders_create
    """
    endpoint = build_endpoint("/v2/checkout/orders")
    headers = build_headers(include_bn_code=True)

    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "custom_id": "Up to 127 characters can go here!",
                "payee": {"merchant_id": request.json["payee_id"]},
                "amount": {
                    "currency_code": "USD",
                    "value": request.json["price"],
                },
            }
        ],
    }

    if include_platform_fees:
        data["purchase_units"][0]["payment_instruction"] = {
            "disbursement_mode": "INSTANT",
            "platform_fees": [{"amount": {"currency_code": "USD", "value": "1.00"}}],
        }

    response = log_and_request("POST", endpoint, headers=headers, data=json.dumps(data))
    response_dict = response.json()
    return jsonify(response_dict)


@bp.route("/capture/<order_id>", methods=("POST",))
def capture(order_id):
    """Capture the order given with the /v2/checkout/orders API.

    Docs: https://developer.paypal.com/docs/api/orders/v2/#orders_capture
    """
    endpoint = build_endpoint(f"/v2/checkout/orders/{order_id}/capture")
    headers = build_headers()

    response = log_and_request("POST", endpoint, headers=headers)
    response_dict = response.json()
    return jsonify(response_dict)


@bp.route("/create-auth-capture", methods=("POST",))
def create_for_auth_capture():
    """Create an order with "intent: AUTHORIZE" with the /v2/checkout/orders API.

    Requires `price` and `payee_id` fields in the request body.

    Docs: https://developer.paypal.com/docs/api/orders/v2/#orders_create
    """
    endpoint = build_endpoint("/v2/checkout/orders")
    headers = build_headers(include_bn_code=True)

    data = {
        "intent": "AUTHORIZE",
        "purchase_units": [
            {
                "custom_id": "Up to 127 characters can go here!",
                "payee": {"merchant_id": request.json["payee_id"]},
                "amount": {
                    "currency_code": "USD",
                    "value": request.json["price"],
                },
            }
        ],
    }

    response = log_and_request("POST", endpoint, headers=headers, data=json.dumps(data))
    response_dict = response.json()
    return jsonify(response_dict)


@bp.route("/auth-capture/<order_id>", methods=("POST",))
def authorize_and_capture_order(order_id):
    """Authorize and then capture the order given."""
    response_dict = authorize_order(order_id)
    auth_id = response_dict["purchase_units"][0]["payments"]["authorizations"][0]["id"]
    return capture_authorization(auth_id)


def authorize_order(order_id):
    """Authorize the order given using the /v2/checkout/orders API.

    Docs: https://developer.paypal.com/docs/api/orders/v2/#orders_authorize
    """

    endpoint = build_endpoint(f"/v2/checkout/orders/{order_id}/authorize")
    headers = build_headers()

    response = log_and_request("POST", endpoint, headers=headers)
    response_dict = response.json()
    return response_dict


def capture_authorization(auth_id, partner_fees=True):
    """Capture the authorization given with the /v2/payments/authorizations API.

    Docs: https://developer.paypal.com/docs/api/payments/v2/#authorizations_capture
    """
    endpoint = build_endpoint(f"/v2/payments/authorizations/{auth_id}/capture")
    headers = build_headers()

    if partner_fees:
        data = {
            "payment_instruction": {
                "disbursement_mode": "INSTANT",
                "platform_fees": [
                    {"amount": {"currency_code": "USD", "value": "1.00"}}
                ],
            }
        }
    else:
        data = {}

    response = log_and_request("POST", endpoint, headers=headers, data=json.dumps(data))
    response_dict = response.json()
    return jsonify(response_dict)


def get_details(order_id):
    """Get the details of the order with the /v2/checkout/orders API.

    Docs: https://developer.paypal.com/docs/api/orders/v2/#orders_get
    """
    endpoint = build_endpoint(f"/v2/checkout/orders/{order_id}")
    headers = build_headers()

    response = log_and_request("GET", endpoint, headers=headers)
    response_dict = response.json()
    return response_dict
