from flask import Blueprint

from api.state import bc
from api.utils.response import ApiError, ApiResponse
from api.utils.validation import validate_json
from api.schemas import BlockUpdateSchema

blocks_bp = Blueprint("blocks", __name__, url_prefix="/blocks")


def _serialize_block(block):
    """Return a JSON-friendly view of a block."""
    return {
        "index": block.index,
        "hash": block.hash,
        "previous_hash": block.previous_hash,
        "difficulty": getattr(block, "difficulty", None),
        "mining_time": getattr(block, "mining_time", None),
        "data": block.data,
    }


def _get_block_or_error(index: int):
    if index < 0 or index >= len(bc.chain):
        return None, ApiResponse(
            error=ApiError.BLOCK_OUT_OF_INDEX,
            status_code=404,
        ).to_response()
    return bc.chain[index], None


@blocks_bp.get("/")
def list_blocks():
    """Return the entire chain as a list of blocks."""
    data = [_serialize_block(block) for block in bc.chain]
    return ApiResponse(data=data).to_response()


@blocks_bp.get("/<int:index>")
def get_block(index: int):
    block, error = _get_block_or_error(index)
    if error:
        return error
    return ApiResponse(data=_serialize_block(block)).to_response()


@blocks_bp.patch("/<int:index>")
@validate_json(BlockUpdateSchema)
def update_block(data, index: int):
    block, error = _get_block_or_error(index)
    if error:
        return error

    block.apply_update(new_previous_hash=data["previous_hash"])
    return ApiResponse(
        data={"message": "Block updated", "length": len(bc.chain)}
    ).to_response()


@blocks_bp.post("/<int:index>/remine")
def remine_block(index: int):
    block, error = _get_block_or_error(index)
    if error:
        return error

    block.mine_block()
    return ApiResponse(data=block.hash).to_response()


@blocks_bp.get("/validation")
def validate_chain():
    return ApiResponse(data={"valid": bc.validate_chain()}).to_response()
