# ref: https://ipapi.is/developers.html

import requests
import json

API_ENDPOINT = "https://api.ipapi.is/?q="


def ip_query(ip: str):
    endpoint = API_ENDPOINT + ip
    res = requests.get(endpoint, timeout=50)
    return json.loads(res.text)


def asn_query(asn: str):
    endpoint = API_ENDPOINT + asn
    res = requests.get(endpoint, timeout=50)
    return json.loads(res.text)
