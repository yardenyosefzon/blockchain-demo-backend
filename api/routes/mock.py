from api.services.mock_data import seed_mock_state
from api.utils.response import ApiResponse

from . import api_bp


@api_bp.post("/mock/seed")
def seed_mock():
    """Rebuild wallets + blockchain with deterministic mock data."""
    data = seed_mock_state()
    return ApiResponse(data=data).to_response()
