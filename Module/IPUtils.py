# ref: https://ipapi.is/developers.html
# ref: https://github.com/ipapi-is/ipapi

import requests

IPAPI_API_ENDPOINT = "https://api.ipapi.is/?q="
SHODAN_INTERNET_DB_ENDPOINT = "https://internetdb.shodan.io/"


def ip_query(ip: str):
    endpoint = IPAPI_API_ENDPOINT + ip
    return requests.get(endpoint, timeout=50).json()


def asn_query(asn: str):
    endpoint = IPAPI_API_ENDPOINT + "as" + asn.strip()
    return requests.get(endpoint, timeout=50).json()


def internet_db_query(ip: str):
    endpoint = SHODAN_INTERNET_DB_ENDPOINT + ip
    return requests.get(endpoint, timeout=50).json()
