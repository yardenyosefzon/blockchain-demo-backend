from flask_cors import CORS


def configure_cors(app):
    origins = app.config.get("CORS_ORIGINS", "*")
    if origins == "*":
        CORS(app)
    else:
        allowed = [o.strip() for o in origins.split(",") if o.strip()]
        CORS(app, resources={r"/*": {"origins": allowed}})
