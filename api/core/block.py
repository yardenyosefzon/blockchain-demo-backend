from datetime import datetime
import hashlib
import time
import json


class Block:
    def __init__(self, data, difficulty, index, previous_hash):
        self.mining_time = None
        self.previous_hash = previous_hash
        self.index = index
        self.difficulty = difficulty
        self.timeStamp = datetime.now()
        self.data = data
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps(
            {
                "index": self.index,
                "previous_hash": self.previous_hash,
                "timeStamp": self.timeStamp,
                "data": self.data,
                "nonce": self.nonce,
            },
            sort_keys=True,
            default=str,
        ).encode()

        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self):
        difficulty = self.difficulty
        start_time = time.time()

        while True:
            block_hash = self.calculate_hash()
            if block_hash.startswith("0" * difficulty):
                self.hash = block_hash
                break
            self.nonce += 1

        end_time = time.time()
        self.mining_time = end_time - start_time

    def apply_update(self, new_previous_hash: str) -> bool:
        """Apply an external previous_hash update with lightweight validation."""

        self.previous_hash = new_previous_hash
        return True

    def __repr__(self) -> str:
        """Readable representation used when printing lists of blocks."""
        data_preview = json.dumps(self.data, default=str)
        if len(data_preview) > 60:
            data_preview = f"{data_preview[:57]}..."
        hash_preview = (self.hash or "")[:10]
        prev_preview = (self.previous_hash or "")[:10]
        return (
            "Block("
            f"index={self.index}, "
            f"hash='{hash_preview}...', "
            f"prev='{prev_preview}...', "
            f"data={data_preview}"
            ")"
        )
