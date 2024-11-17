"""Validation schemas"""
from marshmallow import Schema, fields, post_load
from flask_smorest import abort
from datetime import date, datetime
from dateutil.parser import parse, ParserError


class FlowRateSchema(Schema):
    high = fields.Int(required=True)
    low = fields.Int(required=True)


class ElectricitySchema(Schema):
    date = fields.Str(required=True)
    # noinspection PyTypeChecker
    consume = fields.Nested(FlowRateSchema,required=True)
    # noinspection PyTypeChecker
    supply = fields.Nested(FlowRateSchema,required=True)

    @post_load
    def format_date(self, in_data, **kwargs):
        """Validate and format date 'YYYY-MM-DD'"""
        try:
            in_data["date"] = datetime.strftime(parse(in_data["date"]), "%Y-%m-%d")
            return in_data
        except ParserError as error:
            abort(400, message=str(error))


class PatchElectricitySchema(Schema):
    # noinspection PyTypeChecker
    consume = fields.Nested(FlowRateSchema,load_only=True)
    # noinspection PyTypeChecker
    supply = fields.Nested(FlowRateSchema,load_only=True)


class QueryParamsSchema(Schema):
    start_date = fields.Date(load_default=date(2000,1,1),load_only=True)
    end_date = fields.Date(load_default=date(2100,1,1),load_only=True)


class DeleteAndPatchQueryParamsSchema(Schema):
    date = fields.Date(required=True,load_only=True)