"""Data storage classes for energy usage"""
import redis


class EnergyData:
    """Local Energy Data"""

    def __init__(self):
        """Constructor  energy data"""
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        r = redis.Redis(connection_pool=pool)
        # r.set('location', 'Tolakkerweg136E')
        self._location = r.get('location')


    @property
    def location(self):
        """Getter location energy data"""
        return self._location
