from flask import Blueprint
from core.extensions import db
from core.models import User

auth = Blueprint('auth', __name__)
