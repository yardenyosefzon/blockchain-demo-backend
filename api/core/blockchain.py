import json
from cryptography.hazmat.primitives.asymmetric import ed25519
from flask import Config
from api.core.block import Block


class BlockChain:
    def __init__(
        self,
        difficulty,
        target_block_time,
        retarget_interval,
        alloc_wallet_address,
        block_reward=4,
    ):
        self.chain = []
        self.difficulty = difficulty
        self.target_block_time = target_block_time
        self.retarget_interval = retarget_interval
        self.number_of_blocks = 0
        self.total_mining_time = 0
        self.memory_pool: list[dict] = []
        self.max_txs_per_block: int = 3
        # Use provided block reward (from config) for coinbase
        self.coin_base = block_reward
        self.balances: dict[str, float] = {}
        self.create_genesis_block(alloc_wallet_address)

    def create_genesis_block(self, alloc_wallet_address):
        alloc_value = 50

        genesis_block_data = {
            "type": "genesis",
            "alloc": [{"receiver_address": alloc_wallet_address, "value": alloc_value}],
        }

        block = Block(genesis_block_data, self.difficulty, len(self.chain), "0" * 64)
        block.mine_block()

        self.balances[alloc_wallet_address] = alloc_value
        self.chain.append(block)

    def __add_block(self, block_data):
        if (
            self.number_of_blocks % self.retarget_interval == 0
            and self.number_of_blocks != 0
        ):
            self.update_difficulty()

        previous_hash = self.chain[-1].hash
        block = Block(block_data, self.difficulty, len(self.chain), previous_hash)
        block.mine_block()
        self.balances[block_data["coinbase"]["receiver_address"]] += block_data[
            "coinbase"
        ]["amount"]

        for transaction in block_data["transactions"]:

            sender_balance = self.balances[transaction["sender_address"]]
            receiver_balance = self.balances.get(transaction["receiver_address"])

            if not receiver_balance:
                self.balances[transaction["receiver_address"]] = 0

            self.balances[transaction["sender_address"]] = (
                sender_balance - transaction["amount"] - transaction["fee"]
            )

            self.balances[transaction["receiver_address"]] += transaction["amount"]

        self.total_mining_time += block.mining_time
        self.number_of_blocks += 1
        self.chain.append(block)

    def update_difficulty(self):
        expected = self.target_block_time * self.retarget_interval
        actual = self.total_mining_time
        ratio = actual / expected

        LOWER, UPPER = 0.7, 1.3

        if ratio < LOWER:
            self.difficulty += 1
        elif ratio > UPPER:
            self.difficulty = max(1, self.difficulty - 1)

        # Reset the window for the next interval
        self.total_mining_time = 0

    def validate_chain(self):
        validatedDetails: list = []

        for i in range(0, len(self.chain)):
            valid = True
            current_block = self.chain[i]
            previous_block = self.chain[i - 1] if i > 0 else None

            if current_block.hash != current_block.calculate_hash():
                valid = False
            elif previous_block and current_block.previous_hash != previous_block.hash:
                valid = False
            elif not current_block.hash.startswith("0" * current_block.difficulty):
                valid = False

            blockValidateDetails = {"index": i, "valid": valid}
            validatedDetails.append(blockValidateDetails)

        return validatedDetails

    def submit_signed_tx(self, tx: dict, pub: str, sign: str) -> bool:
        """Verify a signed transaction and enqueue it to the mempool.

        This replaces the older prepare/approve flow by accepting a complete
        transaction dict and its signature, verifying it, and then appending
        to memory_pool if valid.
        """
        # Basic field validation and normalization
        try:
            sender = tx["sender_address"]
            receiver = tx["receiver_address"]
            amount = float(tx["amount"])
            fee = float(tx.get("fee", 0.0))
            note = str(tx.get("note", ""))
        except Exception:
            return False

        # Canonical message for signing
        msg = json.dumps(
            {
                "sender_address": sender,
                "receiver_address": receiver,
                "amount": amount,
                "fee": fee,
                "note": note,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()

        # Verify signature
        try:
            pub_bytes = bytes.fromhex(pub)
            sig_bytes = bytes.fromhex(sign)
            ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes).verify(sig_bytes, msg)
        except Exception:
            return False

        # Funds check using current balances minus pending outflows
        required = amount + fee
        available = self.can_spend(sender)
        if available < required:
            return False

        self.memory_pool.append(
            {
                "sender_address": sender,
                "receiver_address": receiver,
                "amount": amount,
                "fee": fee,
                "note": note,
            }
        )
        return True

    def mine_pending_transactions(self, miner):
        transactions = self.memory_pool[: self.max_txs_per_block]
        total_fees = sum(transaction["fee"] for transaction in transactions)
        coinbase_prize = total_fees + self.coin_base

        block_data = {
            "type": "standard",
            "coinbase": {
                "sender_address": None,
                "receiver_address": miner,
                "amount": coinbase_prize,
            },
            "transactions": transactions,
        }

        self.__add_block(block_data)
        self.memory_pool = self.memory_pool[self.max_txs_per_block :]

    def can_spend(self, address: str) -> float:
        """Return available balance considering pending mempool outflows."""
        balance = float(self.balances.get(address, 0.0))
        awaiting_tx_value = sum(
            float(tx.get("amount", 0.0)) + float(tx.get("fee", 0.0))
            for tx in self.memory_pool
            if tx.get("sender_address") == address
        )

        return balance - awaiting_tx_value

    def pending_balance(self, address: str) -> float:
        """Return future balance considering pending mempool outflows."""
        balance = float(self.balances.get(address, 0.0))
        awaiting_outgoing = sum(
            float(tx.get("amount", 0.0)) + float(tx.get("fee", 0.0))
            for tx in self.memory_pool
            if tx.get("sender_address") == address
        )
        awaiting_incoming = sum(
            float(tx.get("amount", 0.0))
            for tx in self.memory_pool
            if tx.get("receiver_address") == address
        )

        return balance + awaiting_incoming - awaiting_outgoing

    def get_balance(self, address: str) -> float:
        return self.balances[address]

    def reset(self):
        """Resets block chain and wallets"""
        self.chain = []
        self.number_of_blocks = 0
        self.total_mining_time = 0
        self.memory_pool: list[dict] = []
        self.coin_base = Config.BLOCK_REWARD
        self.balances: dict[str, float] = {}

    def __call__(self):
        return self.chain

    def __str__(self):
        chain_data = []

        for block in self.chain:
            chain_data.append(
                {
                    "index": block.index,
                    "previous_hash": block.previous_hash,
                    "timeStamp": block.timeStamp,
                    "data": block.data,
                    "hash": block.hash,
                }
            )

        return json.dumps(chain_data, indent=2, default=str)
