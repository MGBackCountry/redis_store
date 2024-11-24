from datetime import datetime
from flask_smorest import abort
from redis.commands.json.path import Path

from home_db import redis_home as home


class EnergyModel():
    def __init__(self, address_id=None, body_params=None, query_params=None):
        self.address_id = address_id
        self.body_params = body_params
        self.query_params = query_params
        self.dlm = ":"

    def get_electricity(self):
        energy = [home.json().get(address_date)
                  for address_date in home.scan_iter(f"{self.address_id}{self.dlm}*")
                  if self.query_params["start_date"]
                  <= datetime.strptime(address_date.split(self.dlm, 1)[1], "%Y-%m-%d").date()
                  <= self.query_params["end_date"]
                  ]
        if not energy:
            abort(404, message="address not found")
        return energy

    def create_electricity(self):
        adr_dt = f"{self.address_id}{self.dlm}{self.body_params['date']}"
        if home.json().get(adr_dt):
            abort(400, message=f"Entry already exists")
        home.json().set(adr_dt, Path.root_path(), self.body_params)
        return self.body_params

    def update_electricity(self):
        adr_dt = f"{self.address_id}{self.dlm}{self.query_params['date']}"
        energy = home.json().get(adr_dt)
        if not energy:
            abort(404, message="address not found")
        for k, v in self.body_params.items():
            energy[k] = v
        home.json().set(adr_dt, Path.root_path(), energy)
        return energy

    def remove_electricity(self):
        adr_dt = f"{self.address_id}{self.dlm}{self.query_params['date']}"
        if not home.json().get(adr_dt):
            abort(404, message="address not found")
        home.json().delete(adr_dt)
        return
