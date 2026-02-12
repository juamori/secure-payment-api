from flask import Flask
from app.config import Config
from app.extensions import jwt
from app.common.logging import configure_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    configure_logging(app)

    jwt.init_app(app)

    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "ok"}, 200

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.payments.routes import payments_bp
    app.register_blueprint(payments_bp, url_prefix="/payments")

    from app.db.init_db import init_db
    init_db()

    return app
