from __future__ import annotations
from functools import wraps
from typing import Callable, Type
from flask import request
from marshmallow import Schema, ValidationError

from api.utils.response import ApiError, ApiResponse


def validate_json(schema_cls: Type[Schema]) -> Callable:
    """Decorator to validate JSON payloads against a Marshmallow schema."""

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            payload = request.get_json(silent=True)
            if not isinstance(payload, (dict, list)):
                return ApiResponse(error=ApiError.INVALID_JSON).to_response()

            schema = schema_cls(many=isinstance(payload, list))
            try:
                data = schema.load(payload)
            except ValidationError as err:
                return ApiResponse(
                    data={"errors": err.messages},
                    error=ApiError.VALIDATION_FAILED,
                ).to_response()

            return fn(data, *args, **kwargs)

        return wrapper

    return decorator
