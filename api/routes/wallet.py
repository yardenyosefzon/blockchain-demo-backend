from api.core.wallet import Wallet
from api.state import bc, wallets
from api.utils.response import ApiResponse, ApiError
from api.utils.validation import validate_json
from api.schemas import WalletCreateSchema, WalletBalanceSchema

from . import api_bp


@api_bp.get("/wallet")
def list_wallets():
    data = [wallet.to_dict() for wallet in wallets.values()]
    return ApiResponse(data=data).to_response()


@api_bp.post("/wallet/create")
@validate_json(WalletCreateSchema)
def create_wallet(data):
    wallet = Wallet(data["name"])
    wallets[wallet.address] = wallet
    bc.balances[wallet.address] = 0
    return ApiResponse(data=wallet.to_dict(), status_code=201).to_response()


@api_bp.post("/wallet/balance")
@validate_json(WalletBalanceSchema)
def wallet_balance(data):
    address = data["address"]
    if address not in bc.balances:
        return ApiResponse(error=ApiError.ADDRESS_NOT_FOUND).to_response()

    balance = bc.balances[address]
    return ApiResponse(data={"balance": balance}).to_response()
