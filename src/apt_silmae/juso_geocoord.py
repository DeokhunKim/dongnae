import requests
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from .config import config
import json

_config = config['JUSO_GEOCOORD']


def reqeust_coord_by_juso(juso: str):
    apiurl = _config['REQUEST_URL']
    params = {
        "service": "address",
        "request": "getcoord",
        "crs": "epsg:4326",
        "address": juso,
        "format": "json",
        "type": "PARCEL",
        "key": _config['SERVICEKEY']
    }
    response = requests.get(apiurl, params=params)
    if response.status_code == 200:
        load = json.loads(json.dumps(response.json()))
        if load['response']['status'] != 'OK':
            return None
        return load['response']['result']['point']  # dict x, y
    else:
        return None
