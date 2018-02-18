import requests

import datetime

from bahndata import BahnData

class Status(BahnData):

    _url = "status"
    _offline_file = "status.json"

    def get_location(self):
        return (self._data["latitude"], self._data["longitude"])

    def get_time(self):
        return datetime.datetime.fromtimestamp(self._data["serverTime"] / 1000)

    def get_class(self):
        d = {"SECOND": 2,
             "FIRST": 1}
        return d[self._data["wagonClass"]]

    def is_valid_gps(self):
        return self._data['gpsStatus'] == "VALID"
