import hashlib
import json
import math
from cryptography.hazmat.primitives.asymmetric import ed25519

from api.core.blockchain import BlockChain


class Wallet:
    def __init__(self, name):
        self._sk = ed25519.Ed25519PrivateKey.generate()
        self.public = (
            self._sk.public_key().public_bytes_raw().hex()
        )  # 32-byte real pubkey

        h160 = hashlib.new(
            "ripemd160", hashlib.sha256(bytes.fromhex(self.public)).digest()
        ).hexdigest()
        self.address = f"ADDR_{h160}"
        self.name = name

    def sign(self, msg: bytes, secret: str) -> str:
        private_bytes = bytes.fromhex(secret)
        derived_private_key = ed25519.Ed25519PrivateKey.from_private_bytes(
            private_bytes
        )
        return derived_private_key.sign(msg).hex()

    def build_and_sign_tx(
        self,
        tx_payload: dict,
        blockchain: BlockChain,
        secert_to_sign: str,
    ) -> dict | bool:
        """Normalize a tx and sign it using the provided wallet.

        Returns {tx, pub, sign} on success, or False on invalid input.
        """
        # Validate and normalize the payload
        try:
            sender_address = tx_payload["sender_address"]
            receiver_address = tx_payload["receiver_address"]
            amount = float(tx_payload["amount"])
            fee = float(tx_payload.get("fee", 0.0))
            note = str(tx_payload.get("note", ""))
        except Exception:
            return False

        if not isinstance(sender_address, str) or not isinstance(receiver_address, str):
            return False
        if sender_address == "" or receiver_address == "":
            return False
        if not isinstance(note, str):
            return False
        if not math.isfinite(amount) or not math.isfinite(fee):
            return False
        if amount <= 0 or fee < 0:
            return False

        tx = {
            "sender_address": sender_address,
            "receiver_address": receiver_address,
            "amount": amount,
            "fee": fee,
            "note": note,
        }

        # Optional pre-check: ensure funds are available before signing
        required = amount + fee
        available = blockchain.can_spend(sender_address)

        if available < required:
            return False

        # Sign canonical JSON
        msg = json.dumps(tx, sort_keys=True, separators=(",", ":")).encode()
        pub = self.public
        sign = self.sign(msg, secert_to_sign)
        return {"tx": tx, "pub": pub, "sign": sign}

    def to_dict(self) -> dict:
        """Return a JSON-serializable view of the wallet."""

        return {
            "address": self.address,
            "public": self.public,
            "name": self.name,
            "private_key": self._sk.private_bytes_raw().hex(),
        }

    def __repr__(self) -> str:
        return f"Wallet(address={self.address!r}, name={self.name!r})"
