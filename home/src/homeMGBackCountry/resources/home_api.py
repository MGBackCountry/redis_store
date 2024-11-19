"""Endpoint electricity"""
import json
from datetime import datetime

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from home_db import redis
from redis.commands.json.path import Path

from schemas import ElectricitySchema, QueryParamsSchema, DeleteAndPatchQueryParamsSchema, PatchElectricitySchema

blp = Blueprint("HomeApi", __name__, description="ENDPOINT operations on electricity db")

dlm = ":"


@blp.route("/home/<string:address>/electricity")
class HomeApi(MethodView):
    @blp.arguments(ElectricitySchema)
    @blp.response(200)
    def post(self, electricity_data, address):
        address_date = f"{address}{dlm}{electricity_data['date']}"
        if redis.json().get(address_date):
            abort(400, message=f"Entry already exists")
        redis.json().set(address_date, Path.root_path(), electricity_data)
        return electricity_data

    @blp.arguments(QueryParamsSchema, location="query")
    @blp.response(200, ElectricitySchema(many=True))
    # @blp.response(200)
    def get(self, query_params, address):
        electricity_data = [redis.json().get(address_date)
                            for address_date in redis.scan_iter(f"{address}{dlm}*")
                            if query_params["start_date"]
                            <= datetime.strptime(address_date.split(dlm, 1)[1], "%Y-%m-%d").date()
                            <= query_params["end_date"]
                            ]

        if not electricity_data:
            abort(404, message="address not found")
        return electricity_data

    @blp.arguments(DeleteAndPatchQueryParamsSchema, location="query")
    @blp.arguments(PatchElectricitySchema)
    @blp.response(200)
    def patch(self, electricity_path_param, electricity_query_param, address):
        address_date = f"{address}{dlm}{electricity_path_param['date']}"
        electricity_data = redis.json().get(address_date)
        if not electricity_data:
            abort(404, message="address not found")
        for key, value in electricity_query_param.items():
            electricity_data[key] = value
        redis.json().set(address_date, Path.root_path(), electricity_data)
        return electricity_data

    @blp.arguments(DeleteAndPatchQueryParamsSchema, location="query")
    @blp.response(204)
    def delete(self, electricity_data, address):
        address_date = f"{address}{dlm}{electricity_data['date']}"
        if not redis.json().get(address_date):
            abort(404, message="address not found")
        redis.json().delete(address_date)
        return
