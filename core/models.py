from core.extensions import bcrypt, db
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    '''
    stores the user data
    '''
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
