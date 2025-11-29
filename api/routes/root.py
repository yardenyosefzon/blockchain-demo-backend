from api.utils.response import ApiResponse
from . import api_bp


@api_bp.get("/")
def root():
    """Tiny health/info endpoint for quick manual testing."""
    return ApiResponse(
        data={
            "ok": True,
            "service": "blockchain-demo",
            "endpoints": [
                "/v1/chain",
                "/v1/mempool",
                "/v1/transactions",
                "/v1/mine",
                "/v1/mock/seed",
            ],
        }
    ).to_response()
