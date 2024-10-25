"""Endpoint electricity"""
from datetime import datetime
from dateutil.parser import parse, ParserError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request

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
        electricity_data["id"] = el_key
        electricity_db[el_key] = {**electricity_data}

    @blp.response(200, ElectricitySchema(many=True))
    def get(self, address_id):
        start_date = self.get_valid_date(request.args.get("date1"))
        end_date = self.get_valid_date(request.args.get("date2"))

        electricity_output_list = []
        for k,v in electricity_db.items():
            if k.split(":",1)[0] == address_id:
                if not start_date and not end_date:
                    electricity_output_list.append(v)
                elif not end_date:
                    if v['date'] >= start_date:
                        electricity_output_list.append(v)
                elif not start_date:
                    if v['date'] <= end_date:
                        electricity_output_list.append(v)
                else:
                    if start_date <= v['date'] <= end_date:
                        electricity_output_list.append(v)

        if not electricity_output_list:
            abort(404, message="address_id not found")
        return electricity_output_list

    @staticmethod
    def get_valid_date(date):
        if not date:
            return None
        try:
            parse(date)
            try:
                return datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                abort(400, message="format date is not %Y-%m-%d")
        except ParserError:
            abort(400, message="invalid date provided")
