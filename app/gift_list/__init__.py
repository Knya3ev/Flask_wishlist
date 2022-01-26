from flask import Blueprint

gift_list = Blueprint('gift_list', __name__)

from . import views