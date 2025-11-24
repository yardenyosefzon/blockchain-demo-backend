from api.state import wallets
from api.state import bc
from api.utils.response import ApiResponse
from api.utils.validation import validate_json
from api.schemas import PendingBalanceSchema

from . import api_bp


@api_bp.get("/chain")
def chain():
    data = [
        {
            "index": block.index,
            "hash": block.hash,
            "previous_hash": block.previous_hash,
            "difficulty": getattr(block, "difficulty", None),
            "mining_time": getattr(block, "mining_time", None),
            "data": block.data,
        }
        for block in bc.chain
    ]
    return ApiResponse(data=data).to_response()


@api_bp.get("/prize")
def prize():
    return ApiResponse(data={"value": bc.coin_base}).to_response()


@api_bp.get("/mempool")
def mempool():
    mempool_data = getattr(bc, "memory_pool", [])
    return ApiResponse(data=list(mempool_data)).to_response()


@api_bp.get("/validate")
def validate():
    return ApiResponse(data={"valid": bc.validate_chain()}).to_response()


@api_bp.post("/pending_balance")
@validate_json(PendingBalanceSchema)
def can_spend_bulk(data):
    """Return pending_balance values for a provided list of addresses."""
    result = [
        {"address": addr, "value": bc.pending_balance(addr)}
        for addr in data["addresses"]
    ]

    return ApiResponse(data=result).to_response()


@api_bp.get("/reset")
def reset() -> str:
    bc.reset()
    wallets.clear()
    return ApiResponse(data={"message": "Resources reseted"}).to_response()
