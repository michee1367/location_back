from flask import Blueprint
from controllers.ActionController import run_action
from services.auth_service import auth_required
from hashlib import pbkdf2_hmac

action_models = Blueprint('action_models', __name__)

action_models.route("/tables/<table_name>/actions/<name>/record/<record_id>/", methods=["GET"])(run_action)
