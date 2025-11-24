from api.state import bc, wallets
from api.utils.response import ApiResponse, ApiError
from api.utils.validation import validate_json
from api.schemas import TransactionBuildSchema, TransactionApproveSchema

from . import api_bp


@api_bp.post("/transaction/build_sign")
@validate_json(TransactionBuildSchema)
def build_and_sign_transaction(data):
    """Build a canonical transaction and sign it using the backend wallet."""
    wallet = wallets.get(data["sender_address"])
    if wallet is None:
        return ApiResponse(error=ApiError.WALLET_NOT_FOUND).to_response()

    tx_payload = {
        key: data[key]
        for key in ("sender_address", "receiver_address", "amount", "fee", "note")
    }

    result = wallet.build_and_sign_tx(
        tx_payload,
        bc,
        data["private_key"],
    )
    if not result:
        return ApiResponse(error=ApiError.INVALID_TX_PAYLOAD).to_response()

    return ApiResponse(data=result, status_code=201).to_response()


@api_bp.post("/transaction/approve")
@validate_json(TransactionApproveSchema)
def approve_transaction(data):
    """Approve/submit a signed transaction to the mempool."""
    accepted = bc.submit_signed_tx(data["tx"], data["pub"], data["sign"])
    if accepted:
        return ApiResponse(
            data={"accepted": True},
            status_code=201,
        ).to_response()

    return ApiResponse(
        data={"accepted": False},
        error=ApiError.TRANSACTION_REJECTED,
    ).to_response()
