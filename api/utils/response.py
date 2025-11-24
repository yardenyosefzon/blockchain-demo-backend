from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional, Tuple, Union

from flask import jsonify


class ApiError(Enum):
    OK = (0, "")
    INVALID_TX_PAYLOAD = (1001, "invalid payload")
    TRANSACTION_REJECTED = (1002, "Transaction rejected")
    INVALID_JSON = (1003, "Request body must be a valid JSON document")
    ADDRESS_NOT_FOUND = (1004, "Address not found")
    WALLET_NOT_FOUND = (1005, "Wallet not found")
    VALIDATION_FAILED = (1006, "Request validation failed")
    BLOCK_OUT_OF_INDEX = (1007, "Block index out of range")

    def __init__(self, code: int, message: str) -> None:
        self._code = code
        self._message = message

    @property
    def code(self) -> int:
        return self._code

    @property
    def message(self) -> str:
        return self._message

    def to_dict(self) -> Dict[str, Any]:
        return {"code": self.code, "message": self.message}


class ApiResponse:
    """Standard API response envelope with data, error, and success fields."""

    def __init__(
        self,
        data: Any = None,
        error: Optional[Union[ApiError, Dict[str, Any]]] = None,
        status_code: Optional[int] = None,
    ) -> None:
        self.data = data
        if isinstance(error, ApiError):
            self.error = error.to_dict()
        elif error:
            self.error = error
        else:
            self.error = ApiError.OK.to_dict()

        self.success = self.error.get("code", 0) == ApiError.OK.code
        default_status = 200 if self.success else 400
        self.status_code = status_code if status_code is not None else default_status

    def to_response(self) -> Tuple[Any, int]:
        """Convert the envelope into a Flask response tuple."""
        payload = {
            "data": self.data,
            "error": self.error,
            "success": self.success,
        }

        return jsonify(payload), self.status_code
