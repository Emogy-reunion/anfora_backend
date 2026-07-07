from core.extensions import bcrypt, db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
from datetime import timezone


class BaseModel(db.Model):
    '''
    an abstract model to define fields used by all tables
    it won't be created in the database
    '''
    __abstract__ = True

    created_at = db.Column(db.DateTime(timezone=true),
                           server_default=func.now(),
                           nullable=False)
    modified_at = db.Column(db.DateTime(timezone=true),
                            server_default=func.now(),
                            onupdate=func.now(),
                            nullable=False)

class User(BaseModel):
    '''
    stores the user data
    '''
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password, logo):
        '''
        instantializes the table with data
        '''
        self.email = email
        self.password = User.hash_password(password)

    @staticmethod
    def hash_password(self, password):
        '''
        converts the password to a hash for security purposes
        '''
        return bcrypt.generate_password_hash(password).decode('utf-8')
