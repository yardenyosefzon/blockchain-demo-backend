from __future__ import annotations

from marshmallow import EXCLUDE, Schema, ValidationError, fields, validate


class StrippedString(fields.Str):
    """String field that strips whitespace and rejects blanks by default."""

    def __init__(self, *args, allow_blank: bool = False, **kwargs):
        self.allow_blank = allow_blank
        super().__init__(*args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        result = super()._deserialize(value, attr, data, **kwargs)
        stripped = result.strip()
        if not stripped and not self.allow_blank:
            raise ValidationError("Field cannot be blank")
        return stripped


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class WalletCreateSchema(BaseSchema):
    name = StrippedString(required=True)


class WalletBalanceSchema(BaseSchema):
    address = StrippedString(required=True)


class PendingBalanceSchema(BaseSchema):
    addresses = fields.List(
        StrippedString(),
        required=True,
        validate=validate.Length(min=1),
    )


class MinerSchema(BaseSchema):
    miner = StrippedString(required=True)


class TransactionDataSchema(BaseSchema):
    sender_address = StrippedString(required=True)
    receiver_address = StrippedString(required=True)
    amount = fields.Float(
        required=True, validate=validate.Range(min=0, min_inclusive=False)
    )
    fee = fields.Float(load_default=0.0, validate=validate.Range(min=0))
    note = fields.Str(load_default="")


class TransactionBuildSchema(TransactionDataSchema):
    private_key = StrippedString(required=True)


class TransactionApproveSchema(BaseSchema):
    tx = fields.Nested(TransactionDataSchema, required=True)
    pub = StrippedString(required=True)
    sign = StrippedString(required=True)


class BlockUpdateSchema(BaseSchema):
    previous_hash = StrippedString(required=True)


__all__ = [
    "WalletCreateSchema",
    "WalletBalanceSchema",
    "MinerSchema",
    "TransactionBuildSchema",
    "TransactionApproveSchema",
    "BlockUpdateSchema",
]
