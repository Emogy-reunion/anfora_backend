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
    stores the user data
    '''
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    company_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    admin_firstname = db.Column(db.String(255), nullable=False)
    admin_lastname = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
