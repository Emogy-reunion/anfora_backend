from flask import Blueprint, request, jsonify
from core.extensions import db
from core.models import User
from werkzeug.datastructures import MultiDict
from core.forms import RegistrationForm

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    '''
    Creates users accounts
    saves the data to the the database
    '''
    try:
        json_data = request.get_json() or {}

        form = RegistrationForm(data=MultiDict(json_data))

        if not form.validate():
            return jsonify({"errors": form.errors}), 400


        company_name = form.company_name.data.strip().lower()
        email = form.email.data.strip().lower()
        admin_firstname = form.admin_firstname.data.strip().lower()
        admin_lastname = form.admin_lastname.data.strip().lower()
        phone_number = form.phone_number.data.strip()
        password = form.password.data.strip()


        user = db.session.query(User.email).filter_by(email=email).scalar()

        if not user:
            new_user = User(company_name=company_name, email=email, admin_firstname=admin_firstname,
                                admin_lastname=admin_lastname, password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"success": "Account created successfully!"}), 201
        else:
            return jsonify({"error": "An account with this email already exists or cannot be created."}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500


@auth.route('/login', methods=['POST'])
def login():
    '''
    Logs in registered users allowing them to access the members dashboard
    '''
    try:
        json_data = request.get_json() or {}

        form = LoginForm(data=MultiDict(json_data))

        if not form.validate():
            return jsonify({"errors": form.errors}), 400

        email = form.email.data.strip().lower()
        password = form.password.data.strip()

        user = db.session.query(User.id).filter_by(email=email).scalar()

        if user and user.verify_password(password):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            response = jsonify({'success': 'Logged in successfully. Enjoy the experience!'})
            response.status_code == 200
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)

            return response
        else:
            return jsonify({"error": 'Invalid login credentials. Please try again!'}), 400

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred. Please try again!")}, 500


