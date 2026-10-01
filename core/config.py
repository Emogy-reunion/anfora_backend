from dotenv import load_dotenv
import os


load_dotenv()

class Config():
    
    IS_PRODUCTION = os.getenv('FLASK_ENV') == 'production'

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
