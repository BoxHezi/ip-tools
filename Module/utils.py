# ref: https://ipapi.is/developers.html
# ref: https://github.com/ipapi-is/ipapi
# ref: https://internetdb.shodan.io/
import hashlib
import os
import pickle
import zlib
import json

import ipaddress
import requests
from time import strftime
import datetime

IPAPI_API_ENDPOINT = "https://api.ipapi.is/?q="
SHODAN_INTERNET_DB_ENDPOINT = "https://internetdb.shodan.io/"


def ip_query(ip: str):
    endpoint = IPAPI_API_ENDPOINT + ip
    return requests.get(endpoint, timeout=50)


def asn_query(asn: str):
    endpoint = IPAPI_API_ENDPOINT + "as" + asn.strip()
    return requests.get(endpoint, timeout=50)


def internet_db_query(ip: str):
    endpoint = SHODAN_INTERNET_DB_ENDPOINT + ip
    return requests.get(endpoint, timeout=50)


def resp_2_json(resp: requests.models.Response):
    return resp.json()


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


def get_now_datetime():
    return datetime.datetime.now()


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


def cidr2ip(cidr: str, t6: bool = False) -> list:
    """
    convert cidr to ip list
    :param cidr: cidr representation
    :param t6: True if convert target is ipv6 address
    :return: list of ipaddress
    """
    if not t6:
        return [str(ip) for ip in ipaddress.IPv4Network(cidr)]
    return [str(ip) for ip in ipaddress.IPv6Network(cidr)]


def ip_int(ip: str) -> int:
    """
    convert str format ip address to int
    :param ip: ip in string representation
    :return: ip in int
    """
    return int(ipaddress.ip_address(ip))


def ip_str(ip: int) -> str:
    """
    convert int format ip address to str
    :param ip: ip in int representation
    :return: ip in str
    """
    return str(ipaddress.ip_address(ip))


def is_cidr(s: str):
    """
    check if given string is cidr format
    :param s: string to check
    :return: True if in cidr format, False otherwise
    """
    return "/" in s


def list_2_str(ls, delimiter: str = ",") -> str:
    return '' if len(ls) == 0 else delimiter.join(str(i) for i in ls)


def list_2_chunks(ls: list, size: int) -> list[list]:
    return [ls[i: i + size] for i in range(0, len(ls), size)]


def debug_mode():
    return bool(os.getenv("DEBUG"))
