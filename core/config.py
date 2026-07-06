from dotenv import load_dotenv
import os


load_dotenv()

class Config():
    '''
    stores the applications configuration settings
    '''
    IS_PRODUCTION = os.getenv('FLASK_ENV') == 'production'

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
