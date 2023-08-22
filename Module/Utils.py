# ref: https://ipapi.is/developers.html
# ref: https://github.com/ipapi-is/ipapi
# ref: https://internetdb.shodan.io/

import os
import requests
from time import strftime

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


def get_all_country_code():
    ipv4_path = "./country-ip-blocks/ipv4/"
    ipv6_path = "./country-ip-blocks/ipv6/"
    country_set = set()
    for country in os.listdir(ipv4_path) + os.listdir(ipv6_path):
        country_set.add(country[0:2])

    return list(country_set)


def get_current_time():
    return strftime("%Y-%m-%d %H:%M:%S")
