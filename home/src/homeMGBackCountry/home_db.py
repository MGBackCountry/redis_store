"""home_db.py
Purpose: Connect to redis database
"""
from os import environ
from redis import Redis

redis_home = Redis(host=environ.get("REDIS_HOST"), port=environ.get("REDIS_PORT"),
                   decode_responses=True)
