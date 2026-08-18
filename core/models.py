from core.extensions import bcrypt, db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
from datetime import timezone
import uuid


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
