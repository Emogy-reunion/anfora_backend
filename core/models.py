from core.extensions import bcrypt, db
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
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
