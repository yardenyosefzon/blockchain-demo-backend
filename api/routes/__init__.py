from flask import Blueprint

api_bp = Blueprint("v1", __name__)

# Import route handlers so they register with the blueprint.
from . import (
    blockchain,
    block,
    mining,
    mock,
    root,
    transactions,
    wallet,
)  # noqa: E402,F401

__all__ = ["api_bp"]
