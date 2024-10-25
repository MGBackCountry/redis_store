"""Validation schemas"""
from marshmallow import Schema, fields


class FlowRateSchema(Schema):
    high = fields.Int(required=True)
    low = fields.Int(required=True)


class ElectricitySchema(Schema):
    id = fields.Str(dump_only=True)
    date = fields.Date(required=True)
    # noinspection PyTypeChecker
    consume = fields.Nested(FlowRateSchema,required=True)
    # noinspection PyTypeChecker
    supply = fields.Nested(FlowRateSchema,required=True)
