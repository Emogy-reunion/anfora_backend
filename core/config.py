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

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLs = True
    MAIL_USERNAME = os.getenv('EMAIL')
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('EMAIL')
    MAIL_ASCII_ATTACHMENTS = False
    MAIL_MAX_EMAILS = None
