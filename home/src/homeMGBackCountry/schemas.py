"""Validation schemas"""
from marshmallow import Schema, fields
from datetime import date


class FlowRateSchema(Schema):
    high = fields.Int(required=True)
    low = fields.Int(required=True)


class ElectricitySchema(Schema):
    date = fields.Str(required=True)
    # noinspection PyTypeChecker
    consume = fields.Nested(FlowRateSchema,required=True)
    # noinspection PyTypeChecker
    supply = fields.Nested(FlowRateSchema,required=True)


class PatchElectricitySchema(Schema):
    # noinspection PyTypeChecker
    consume = fields.Nested(FlowRateSchema)
    # noinspection PyTypeChecker
    supply = fields.Nested(FlowRateSchema)


class QueryParamsSchema(Schema):
    start_date = fields.Date(load_default=date(2000,1,1),load_only=True)
    end_date = fields.Date(load_default=date(2100,1,1),load_only=True)


class DeletePatchQueryParamsSchema(Schema):
    date = fields.Date(required=True)