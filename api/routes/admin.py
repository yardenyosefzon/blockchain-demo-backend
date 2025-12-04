from flask import Blueprint

from api.services.mock_data import seed_mock_state
from api.state import bc, wallets
from api.utils.response import ApiResponse

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.post("/reset")
def reset_state():
    """Reset in-memory blockchain and wallets."""
    bc.reset()
    wallets.clear()
    return ApiResponse(data={"message": "Resources reseted"}).to_response()


@admin_bp.post("/mock-seed")
def seed_mock():
    """Rebuild wallets + blockchain with deterministic mock data."""
    data = seed_mock_state()
    return ApiResponse(data=data).to_response()
