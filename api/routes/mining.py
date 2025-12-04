from flask import Blueprint

from api.state import bc
from api.utils.response import ApiResponse
from api.utils.validation import validate_json
from api.schemas import MinerSchema

mining_bp = Blueprint("mining", __name__, url_prefix="/mining")


@mining_bp.post("/blocks")
@validate_json(MinerSchema)
def mine_block(data):
    """Mine pending transactions into a new block."""
    bc.mine_pending_transactions(data["miner"])
    return ApiResponse(data={"status": "mined"}, status_code=201).to_response()


@mining_bp.get("/reward")
def mining_reward():
    return ApiResponse(data={"value": bc.coin_base}).to_response()
