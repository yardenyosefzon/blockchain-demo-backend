# services/miner.py
import time
from api.state import bc  # import the singleton blockchain


def mine_forever(miner_address: str, interval: int = 5):
    """
    Keep mining blocks in a loop.
    - miner_address: address that will receive the coinbase reward
    - interval: how often to check the mempool (seconds)
    """
    while True:
        if bc.memory_pool:  # if there are transactions waiting
            bc.mine_pending_transactions(miner_address)
            print(
                f"[miner] New block mined for {miner_address}. Chain length: {len(bc.chain)}"
            )
        else:
            print("[miner] Mempool empty, waiting...")

        time.sleep(interval)
