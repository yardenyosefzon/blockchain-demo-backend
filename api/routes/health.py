from flask import Blueprint

from api.utils.response import ApiResponse

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    """Simple health check endpoint."""
    return ApiResponse(
        data={
            "ok": True,
            "service": "blockchain-demo",
        }
    ).to_response()
