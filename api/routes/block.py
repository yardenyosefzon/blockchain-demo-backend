from api.state import bc
from api.utils.response import ApiResponse, ApiError
from api.utils.validation import validate_json
from api.schemas import ChainBlockSchema, RemineBlockSchema

from . import api_bp


@api_bp.post("/block")
@validate_json(ChainBlockSchema)
def update_block(data):
    block_data = data

    idx = int(block_data["index"])
    new_previous_hash = block_data["previous_hash"]

    if idx < 0 or idx >= len(bc.chain):
        return ApiResponse(data={"error": ApiError.BLOCK_OUT_OF_INDEX}, status_code=400)

    block = bc.chain[idx]
    block.apply_update(new_previous_hash=new_previous_hash)

    return ApiResponse(
        data={"message": "Block updated", "length": len(bc.chain)}
    ).to_response()


@api_bp.post("/block/remine")
@validate_json(RemineBlockSchema)
def remine_block(data):
    block_data = data

    idx = int(block_data["index"])
    block = bc.chain[idx]
    block.mine_block()
    return ApiResponse(data=block.hash).to_response()
