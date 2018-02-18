import requests

import json
import datetime

class BahnData:

    _url = None
    _hostname = "https://iceportal.de/api1/rs/"
    #_hostname = "http://localhost:5000/"
    _offline_file = None
    _data = None

    def __init__(self, offline=False):
        self.offline = offline
        self.update()

    def update(self):
        assert self._url is not None
        assert self._offline_file is not None
        assert self._hostname is not None

        if not self.offline:
            try:
                self._data = requests.get(self._hostname + self._url).json()
            except Exception as e:
                if self._data is None:
                    with open(self._offline_file) as ofile:
                        self._data = json.load(ofile)
        else:
            with open(self._offline_file) as ofile:
                self._data = json.load(ofile)

    def __getitem__(self, name):
        if hasattr(self, "get_{}".format(name)):
            return getattr(self, "get_{}".format(name))
        elif hasattr(self, name):
            return self.getattr(name)
        elif name in self._data:
            return self._data[name]
        else:
            raise AttributeError
