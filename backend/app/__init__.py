from flask import Flask

from .auth import validate_service_token


def create_app():
    app = Flask(__name__)

    # Force all endpoints to validate token
    @app.before_request
    def authenticate():
        return validate_service_token()

    from .routes.hello import hello

    app.register_blueprint(hello)

    return app
