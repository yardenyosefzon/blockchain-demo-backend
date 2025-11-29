from __future__ import annotations

from api.core.blockchain import BlockChain
from api.core.wallet import Wallet
from api.state import bc, wallets


def _serialize_chain(blockchain: BlockChain) -> list[dict]:
    return [
        {
            "index": block.index,
            "hash": block.hash,
            "previous_hash": block.previous_hash,
            "difficulty": getattr(block, "difficulty", None),
            "mining_time": getattr(block, "mining_time", None),
            "data": block.data,
        }
        for block in blockchain.chain
    ]


def seed_mock_state() -> dict:
    """Reset blockchain + wallets and populate consistent mock data."""

    wallets.clear()

    demo_wallets = {
        "alice": Wallet("Alice"),
        "bob": Wallet("Bob"),
        "charlie": Wallet("Charlie"),
        "miner": Wallet("Miner"),
    }

    for wallet in demo_wallets.values():
        wallets[wallet.address] = wallet

    # Rebuild the chain starting from a fresh genesis block.
    bc.reset(demo_wallets["alice"].address)
    for wallet in demo_wallets.values():
        bc.balances.setdefault(wallet.address, 0.0)

    block1_txs = [
        {
            "sender_address": demo_wallets["alice"].address,
            "receiver_address": demo_wallets["bob"].address,
            "amount": 15.0,
            "fee": 1.0,
            "note": "Alice pays Bob for setup work",
        },
        {
            "sender_address": demo_wallets["alice"].address,
            "receiver_address": demo_wallets["charlie"].address,
            "amount": 5.0,
            "fee": 0.5,
            "note": "Starter funds for Charlie",
        },
    ]
    block1_fees = sum(tx["fee"] for tx in block1_txs)

    block2_txs = [
        {
            "sender_address": demo_wallets["bob"].address,
            "receiver_address": demo_wallets["alice"].address,
            "amount": 5.0,
            "fee": 0.5,
            "note": "Bob reimburses Alice",
        },
        {
            "sender_address": demo_wallets["charlie"].address,
            "receiver_address": demo_wallets["bob"].address,
            "amount": 2.0,
            "fee": 0.2,
            "note": "Charlie pays Bob",
        },
    ]
    block2_fees = sum(tx["fee"] for tx in block2_txs)

    bc.mine_block_from_data(
        {
            "type": "standard",
            "coinbase": {
                "sender_address": None,
                "receiver_address": demo_wallets["miner"].address,
                "amount": bc.coin_base + block1_fees,
            },
            "transactions": block1_txs,
        }
    )
    bc.mine_block_from_data(
        {
            "type": "standard",
            "coinbase": {
                "sender_address": None,
                "receiver_address": demo_wallets["miner"].address,
                "amount": bc.coin_base + block2_fees,
            },
            "transactions": block2_txs,
        }
    )

    # Pending mempool transactions that respect the available balances above.
    bc.memory_pool = [
        {
            "sender_address": demo_wallets["bob"].address,
            "receiver_address": demo_wallets["charlie"].address,
            "amount": 3.0,
            "fee": 0.1,
            "note": "Bob tops up Charlie",
        },
        {
            "sender_address": demo_wallets["alice"].address,
            "receiver_address": demo_wallets["miner"].address,
            "amount": 2.0,
            "fee": 0.2,
            "note": "Alice tips the miner",
        },
    ]

    return {
        "wallets": [wallet.to_dict() for wallet in demo_wallets.values()],
        "balances": dict(bc.balances),
        "chain": _serialize_chain(bc),
        "mempool": list(bc.memory_pool),
    }
