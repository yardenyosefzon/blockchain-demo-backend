from flask import Blueprint

from .admin import admin_bp
from .blocks import blocks_bp
from .health import health_bp
from .mining import mining_bp
from .transactions import transactions_bp
from .wallets import wallets_bp

api_v1_bp = Blueprint("api_v1", __name__)

# Register sub-blueprints with grouped prefixes
api_v1_bp.register_blueprint(blocks_bp)
api_v1_bp.register_blueprint(mining_bp)
api_v1_bp.register_blueprint(transactions_bp)
api_v1_bp.register_blueprint(wallets_bp)
api_v1_bp.register_blueprint(admin_bp)
api_v1_bp.register_blueprint(health_bp)

__all__ = ["api_v1_bp"]
