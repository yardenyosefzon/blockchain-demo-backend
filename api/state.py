# state.py
from api.config.env import Config
from api.core.blockchain import BlockChain
from api.core.wallet import Wallet

# First wallet for alloc
firstWalletEver = "Adam"
w = Wallet(firstWalletEver)

wallets: dict[str, Wallet] = {w.address: w}  # address -> Wallet instance

# Single, in-memory node state
bc = BlockChain(
    difficulty=Config.DIFFICULTY,
    target_block_time=Config.TARGET_BLOCK_TIME,
    retarget_interval=Config.RETARGET_INTERVAL,
    alloc_wallet_address=w.address,
    block_reward=Config.BLOCK_REWARD,
)
