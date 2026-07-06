from Flask import flask


def create_app():
    """
    creates the application instance
    """

    app = Flask(__name__)

    return app
