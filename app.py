# app.py
from flask import Flask
from api.config.env import Config
from api.extensions import init_extensions
from api.routes import api_bp


def create_app() -> Flask:
    """Application factory: creates and configures the Flask app.
    This lets you scale later and keeps tests simple.
    """
    app = Flask(__name__)

    init_extensions(app)

    # App-level config from environment
    app.config.from_object(Config)

    # Register REST API blueprint under /api
    app.register_blueprint(api_bp, url_prefix="/v1")

    # Initialize extensions (e.g., CORS)
    return app


# Create the app instance for `flask run` or `python app.py`
app = create_app()

if __name__ == "__main__":
    # Run the dev server only when executing `python app.py`
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host="0.0.0.0")


# run to be on right venv -
# source "/Users/yardenyosefzon/Developer/פרויקטים/python projects/blockcahin demo/.venv/bin/activate"
