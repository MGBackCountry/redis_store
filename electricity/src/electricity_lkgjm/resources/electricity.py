"""Endpoint electricity"""
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import electricity_db
from schemas import ElectricitySchema


blp = Blueprint("Electricity", __name__, description="ENDPOINT operations on electricity db")


@blp.route("/electricity/<string:address_id>")
class Electricity(MethodView):
    @blp.arguments(ElectricitySchema)
    @blp.response(200, ElectricitySchema)
    def post(self, electricity_data, address_id):
        el_key = f"{address_id}:{str(electricity_data['date'])}"
        if el_key in electricity_db.keys():
            abort(400, message=f"Entry already exists")
        electricity_db[el_key] = {**electricity_data, "id:": address_id}
        return electricity_db[el_key]

    @blp.response(200, ElectricitySchema(many=True))
    def get(self, address_id):
        electricity_output_list = []
        for k,v in electricity_db.items():
            if k.split(":",1)[0] == address_id:
                electricity_output_list.append(v)
        if not electricity_output_list:
            abort(404, message="address_id not found")
        return electricity_output_list
