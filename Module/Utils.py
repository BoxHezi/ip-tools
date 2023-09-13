# ref: https://ipapi.is/developers.html
# ref: https://github.com/ipapi-is/ipapi
# ref: https://internetdb.shodan.io/
import hashlib
import os
import pickle
import zlib
import json

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


def read_file(file_path: str, binary: bool = False) -> list | None:
    """
    read file content and return a list of file contents, separate by newline
    :param file_path: path to file to be read
    :param binary: reading in binary mode, False by default
    :return: file contents, None if file not found
    """
    try:
        with open(file_path, "r" if not binary else "rb") as reader:
            return [line.strip() for line in reader]
    except FileNotFoundError as e:
        print(e)
        return None


def cal_hash(data: bytes):
    """
    calculate hash for data
    return a tuple with length of 2, contains md5 hash and sha256 hash
    :param data: data to calculate hash for
    :return: size 2 tuple, (md5, sha256)
    """
    try:
        return hashlib.md5(data).hexdigest(), hashlib.sha256(data).hexdigest()
    except Exception as e:
        print(e)
        return None


def compare_obj(obj1: bytes, obj2: bytes):
    return cal_hash(obj1) == cal_hash(obj2)


def get_current_time():
    return strftime("%Y-%m-%d %H:%M:%S")


def serialize(obj: object):
    return pickle.dumps(obj)


def deserialize(data: bytes):
    return pickle.loads(data)


def compress(data: bytes):
    return zlib.compress(data)


def decompress(data: bytes):
    return zlib.decompress(data)


def to_json(data: str):
    return json.loads(data)


def to_str(data: dict):
    return json.dumps(data)
