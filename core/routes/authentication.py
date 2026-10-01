import uuid
from flask import Blueprint, request, jsonify
from core.extensions import db, bcrypt
from core.models import User
from core.forms.RegistrationForm import RegistrationForm, LoginForm
from werkzeug.datastructures import MultiDict
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    jwt_required,
    get_jwt_identity,
)

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    '''
    Creates user accounts and saves the data to the database
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
        raw_password = form.password.data.strip()

        existing_user = db.session.query(User).filter_by(email=email).first()

        if not existing_user:
            # Pass raw_password directly so the model setter handles hashing once cleanly
            new_user = User(
                company_name=company_name,
                email=email,
                admin_firstname=admin_firstname,
                admin_lastname=admin_lastname,
                phone_number=phone_number,
                password=raw_password  
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"success": "Account created successfully!"}), 201
        else:
            return jsonify({"error": "An account with this email already exists."}), 400

    except Exception as e:
        db.session.rollback()
        print(f"REGISTRATION ERROR: {str(e)}")  
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@auth.route('/login', methods=['POST'])
def login():
    '''
    Logs in registered users and sets JWT cookies
    '''
    try:
        json_data = request.get_json() or {}
        form = LoginForm(data=MultiDict(json_data))

        if not form.validate():
            return jsonify({"errors": form.errors}), 400

        email = form.email.data.strip().lower()
        password = form.password.data.strip()

        
        user = db.session.query(User).filter_by(email=email).first()

        if user and user.verify_password(password):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            response = jsonify({'success': 'Logged in successfully. Enjoy the experience!'})
            response.status_code = 200  # Fixed assignment operator
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)

            return response
        else:
            return jsonify({"error": 'Invalid login credentials. Please try again!'}), 400

    except Exception as e:
        print(f"Login ERROR: {str(e)}")  
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@auth.route('/refresh_token', methods=['POST'])
@jwt_required(refresh=True)  # Fixed decorator name
def refresh_token():
    '''
    Refreshes the access token after it expires
    '''
    try:
        current_identity = get_jwt_identity()
        user_id = uuid.UUID(current_identity)  # Assuming UUID primary key; change to int(current_identity) if IDs are integers

        user = db.session.query(User).filter_by(id=user_id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        access_token = create_access_token(identity=str(user.id))
        
        response = jsonify({"success": "Token refreshed successfully!"})
        response.status_code = 200
        set_access_cookies(response, access_token)

        return response
    except Exception as e:
        return jsonify({"error": 'An unexpected error occurred. Please try again!'}), 500