from flask_cors import CORS
from api.config.cors import configure_cors

# Instantiate extensions here (so they can be imported elsewhere if needed)
cors = CORS()


def init_extensions(app):
    """Initialize Flask extensions with app config.

    This follows the common Flask pattern of creating extension instances
    at module scope and initializing them in an `init_app` function.
    """
    configure_cors(app)
    app.url_map.strict_slashes = False


# …register blueprints, routes, etc.
