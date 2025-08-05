"""API Endpoint electricity"""
from flask.views import MethodView
from flask_smorest import Blueprint

from electricity.model.home import EnergyModel
from electricity.schemas import ElectricitySchema, QueryParamsSchema, DeleteAndPatchQueryParamsSchema, PatchElectricitySchema

blp = Blueprint("HomeApi", __name__, description="ENDPOINT operations on electricity db")


@blp.route("/home/<string:address_id>/electricity")
class HomeEnergy(MethodView):
    @blp.arguments(QueryParamsSchema, location="query")
    @blp.response(200, ElectricitySchema(many=True),
                  example={"date": "2024-11-20",
                           "consume": {"low": 140, "high": 250},
                           "supply": {"low": 50, "high": 120}})
    def get(self, query_params, address_id):
        energy = EnergyModel(address_id, None, query_params)
        return energy.get_electricity()

    @blp.arguments(ElectricitySchema,
                   example={"date": "2024-11-20",
                            "consume": {"low": 140, "high": 250},
                            "supply": {"low": 50, "high": 120}
                            })
    @blp.response(200)
    def post(self, electricity_data, address_id):
        energy = EnergyModel(address_id, electricity_data)
        return energy.create_electricity()

    @blp.arguments(DeleteAndPatchQueryParamsSchema, location="query")
    @blp.arguments(PatchElectricitySchema, example={"consume": {"low": 144, "high": 255},
                                                    "supply": {"low": 55, "high": 125}})
    @blp.response(200)
    def patch(self, query_params, body_params, address_id):
        energy = EnergyModel(address_id, body_params, query_params)
        return energy.update_electricity()

    @blp.arguments(DeleteAndPatchQueryParamsSchema, location="query")
    @blp.response(204)
    def delete(self, query_params, address_id):
        energy = EnergyModel(address_id, None, query_params)
        return energy.remove_electricity()
