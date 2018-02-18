import requests

import datetime

from bahndata import BahnData

class TripInfo(BahnData):
    _url = "tripInfo"
    _offline_file = "tripInfo.json"

    def get_stop_by_evanr(self, evanr):
        for stop in self._data["stops"]:
            if stop["station"]["evaNr"].startswith(evanr):
                return stop
