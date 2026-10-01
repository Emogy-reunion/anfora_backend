from flask import Flask
from core.extensions import db,jwt,bcrypt,migrate
from core.routes.authentication import auth as auth_bp
from Routes.Costing_Sheet import costings_bp
from Routes.Invoice import invoices_bp
from Routes.Quotation import quotations_bp
from Routes.Itinerary import itineraries_bp
from Routes.Booking import bookings_bp
from Routes.supplier import suppliers_bp
from core.config import Config

def create_app():
    app = Flask(__name__)
    
    
    app.config.from_object(Config)

    
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] 
    
    if not app.config.get("SQLALCHEMY_TRACK_MODIFICATIONS"):
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] 

    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app)
    jwt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(costings_bp, url_prefix="/api")
    app.register_blueprint(invoices_bp, url_prefix="/api")
    app.register_blueprint(quotations_bp, url_prefix="/api")
    app.register_blueprint(itineraries_bp, url_prefix="/api")
    app.register_blueprint(bookings_bp, url_prefix="/api")
    app.register_blueprint(suppliers_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)