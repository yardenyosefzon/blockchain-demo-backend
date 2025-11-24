from api.state import bc
from api.utils.response import ApiResponse
from api.utils.validation import validate_json
from api.schemas import MinerSchema

from . import api_bp


@api_bp.post("/mine")
@validate_json(MinerSchema)
def mine(data):
    bc.mine_pending_transactions(data["miner"])
    return ApiResponse(data={"status": "mined"}, status_code=201).to_response()
