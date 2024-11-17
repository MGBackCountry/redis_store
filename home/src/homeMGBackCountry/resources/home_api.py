"""Endpoint electricity"""
import json
from datetime import datetime

from dateutil.parser import parse, ParserError
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from home_db import redis
from redis.commands.json.path import Path

from schemas import ElectricitySchema, QueryParamsSchema, DeletePatchQueryParamsSchema, PatchElectricitySchema

blp = Blueprint("HomeApi", __name__, description="ENDPOINT operations on electricity db")

dlm = ":"


@blp.route("/home/<string:address>/electricity")
class HomeApi(MethodView):
    @blp.arguments(ElectricitySchema)
    @blp.response(200)
    def post(self, electricity_data, address):
        electricity_data["date"] = self.format_date(electricity_data["date"])
        address_date = f"{address}{dlm}{electricity_data['date']}"
        if redis.json().get(address_date):
            abort(400, message=f"Entry already exists")
        redis.json().set(address_date, Path.root_path(), json.dumps(electricity_data))
        return electricity_data

    @blp.arguments(QueryParamsSchema, location="query")
    @blp.response(200, ElectricitySchema(many=True))
    def get(self, query_params, address):
        electricity_data = [json.loads(redis.json().get(address_date))
                            for address_date in redis.scan_iter(f"{address}{dlm}*")
                            if query_params["start_date"]
                            <= datetime.strptime(address_date.split(dlm, 1)[1], "%Y-%m-%d").date()
                            <= query_params["end_date"]
                            ]

        if not electricity_data:
            abort(404, message="address not found")
        return electricity_data

    @blp.arguments(DeletePatchQueryParamsSchema, location="query")
    @blp.arguments(PatchElectricitySchema)
    @blp.response(200, ElectricitySchema)
    def patch(self, electricity_path_param, electricity_query_param, address):
        address_date = f"{address}{dlm}{electricity_path_param['date']}"
        electricity_data = redis.json().get(address_date)
        if not electricity_data:
            abort(404, message="address not found")
        electricity_dict = json.loads(electricity_data)
        for key, value in electricity_query_param.items():
            electricity_dict[key] = value
        redis.json().set(address_date, Path.root_path(), json.dumps(electricity_dict))
        return electricity_dict

    @blp.arguments(DeletePatchQueryParamsSchema, location="query")
    @blp.response(204)
    def delete(self, electricity_data, address):
        address_date = f"{address}{dlm}{electricity_data['date']}"
        if not redis.json().get(address_date):
            abort(404, message="address not found")
        redis.json().delete(address_date)
        return

    @staticmethod
    def format_date(date_str):
        """Validate and format date 'YYYY-MM-DD'"""
        try:
            return datetime.strftime(parse(date_str), "%Y-%m-%d")
        except ParserError as error:
            abort(400, message=str(error))
