from Flask import flask
from core.extensions import db, bcrypt, jwt, migrate
from core.config import Config


def create_app():
    """
    creates the application instance
    """

    app = Flask(__name__)

    app.config.from_object(Config)
    
    #initialize extensions
    db.init_app()
    bcrypt.init_app()
    jwt.init_app()
    migrate.init_app(app, db)

    return app
