from flask import Blueprint

from api.core.wallet import Wallet
from api.state import bc, wallets
from api.utils.response import ApiError, ApiResponse
from api.utils.validation import validate_json
from api.schemas import PendingBalanceSchema, WalletCreateSchema

wallets_bp = Blueprint("wallets", __name__, url_prefix="/wallets")


def _wallet_or_error(address: str):
    wallet = wallets.get(address)
    if wallet is None:
        return None, ApiResponse(error=ApiError.WALLET_NOT_FOUND, status_code=404).to_response()
    return wallet, None


def _wallet_data(wallet: Wallet) -> dict:
    """Return the full wallet dict including secret key."""
    return wallet.to_dict()


@wallets_bp.get("/")
def list_wallets():
    data = [_wallet_data(wallet) for wallet in wallets.values()]
    return ApiResponse(data=data).to_response()


@wallets_bp.post("/")
@validate_json(WalletCreateSchema)
def create_wallet(data):
    wallet = Wallet(data["name"])
    wallets[wallet.address] = wallet
    bc.balances[wallet.address] = 0
    return ApiResponse(data=_wallet_data(wallet), status_code=201).to_response()


@wallets_bp.get("/<address>")
def get_wallet(address: str):
    wallet, error = _wallet_or_error(address)
    if error:
        return error
    return ApiResponse(data=_wallet_data(wallet)).to_response()


@wallets_bp.get("/<address>/balance")
def wallet_balance(address: str):
    if address not in bc.balances:
        return ApiResponse(error=ApiError.ADDRESS_NOT_FOUND, status_code=404).to_response()

    balance = bc.balances[address]
    return ApiResponse(data={"balance": balance}).to_response()


@wallets_bp.post("/pending-balances")
@validate_json(PendingBalanceSchema)
def pending_balances(data):
    """Return pending_balance values for a provided list of addresses."""
    result = [
        {"address": addr, "value": bc.pending_balance(addr)}
        for addr in data["addresses"]
    ]

    return ApiResponse(data=result).to_response()
