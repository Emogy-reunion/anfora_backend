from core.extensions import bcrypt, db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
from datetime import timezone
import uuid
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


SALT = 'email-verification'


class BaseModel(db.Model):
    '''
    an abstract model to define fields used by all tables
    it won't be created in the database
    '''
    __abstract__ = True

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),
                           nullable=False)
    modified_at = db.Column(db.DateTime(timezone=True),
                            server_default=func.now(),
                            onupdate=func.now(),
                            nullable=False)

class User(BaseModel):
    '''
    stores the company's authentication data
    '''
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    company_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    admin_firstname = db.Column(db.String(255), nullable=False)
    admin_lastname = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, password=None, **kwargs):
        super().__init__(**kwargs)

        if password:
            self.password = password

    @property
    def password(self):
        raise AttributeError("Password is write-only and cannot be read.")

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password)

    @staticmethod
    def _get_serializer():
        '''
        initializes and returns the serializer
        '''
        return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    def generate_verification_token(self):
        return self._get_serializer().dumps({'user_id': str(self.id)}, salt=SALT)

    @staticmethod
    def verify_token(token):
        '''
        deserializes the token and retrieves the user id
        queris the database and returns the user if they exist
        '''
        try:
            data = User._get_serializer().loads(token, salt=SALT, max_age=3600)
            user_id = uuid.UUID(data['user_id'])
            user = db.session.get(User, user_id)

            if user:
                return user
            else:
                return None
        except (BadSignature, SignatureExpired, ValueError, TypeError, KeyError):
            return None




class Profile(BaseModel):
    '''
    stores the company's profile information data
    '''
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    logo_url = db.Column(db.String(255), nullable=False)
    address_line1 = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(3), nullable=False)
    default_currency = db.Column(db.String(3), nullable=False)

    website = db.Column(db.String(255), nullable=True)
    legal_business_name = db.Column(db.String(255), nullable=True)
    tax_identification_number = db.Column(db.String(100), nullable=True)
    default_payment_terms = db.Column(db.Integer, default=30, nullable=False)
    default_notes = db.Column(db.Text, nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    address_line2 = db.Column(db.String(255), nullable=True)
