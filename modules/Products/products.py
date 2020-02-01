from flask import Blueprint

account_apis = Blueprint('account_api', __name__)

@account_apis.route("/account")
def accountList():
    return "list of accounts"