import requests

from zipfile import ZipFile
from io import BytesIO

from Module.SqliteDriver import DB

import time

import nvdlib
import ares  # python wrapper for https://www.circl.lu/services/cve-search/


# NIST NVD CVE API reference: https://nvd.nist.gov/developers/vulnerabilities
# NVDLib Documentation: https://nvdlib.com/en/latest/v1/v1.html#search-cpe

# CAPEC CSV: https://capec.mitre.org/data/csv/2000.csv.zip
# CWE CSV: https://cwe.mitre.org/data/csv/2000.csv.zip


def start_cve_search(db: DB):
    query = """SELECT * FROM internetdb WHERE vulns != '';"""
    db.cursor.execute(query)
    results = db.cursor.fetchall()
    potential_targets = set()
    cve_search = ares.CVESearch()
    # checked_cve = {}
    for i in range(len(results)):
        record = results[i]
        cves = record[5].split(",")
        if content_high_cve(cve_search, cves):
            hostnames = record[2].split(",")
            potential_targets.update(hostnames)

        # for cve in cves.split(","):
        #     try:
        #         cve_result = cve_search.id(cve)
        #         cvss = cve_result['cvss']
        #         print(f"{cve} - CVSS: {cvss}")
        #         if cvss and cvss > 7:
        #             hostnames = record[2].split(",")
        #             potential_targets.update(hostnames)
        #     except (ConnectionError, RemoteDisconnected) as e:
        #         print(f"Exception: {e}")
    return potential_targets


def content_high_cve(cve_search: ares.CVESearch, cves: list):
    for cve in cves:
        try:
            cve_result = cve_search.id(cve)
            cvss = cve_result["cvss"]
            print(f"{cve} - CVSS: {cvss}")
            if cvss and cvss > 7:
                return True
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Exception: {e} for CVE: {cve}")
    return False

# def search_cve(cve_id: str):
#     # CIRCL_BASE_URL = "https://cve.circl.lu/api/cve/"
#     NIST_NVD_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
#     url = f"{NIST_NVD_BASE_URL}?cveId={cve_id}"
#     resp = requests.get(url)
#     resp.raise_for_status()
#     # pprint.pprint(resp.json())
#     return resp.json()



# def search_cpe(cpe_name: str):
#     pass


def download_local_db():
    download_file("https://capec.mitre.org/data/csv/2000.csv.zip", "capec")
    download_file("https://cwe.mitre.org/data/csv/2000.csv.zip", "cwe")


def download_file(url: str, to_download: str):
    print(f"Downloading {to_download.upper()} database...")

    local_name_prefix = "./databases/" + to_download
    resp = requests.get(url)
    my_zip = ZipFile(BytesIO(resp.content))

    for zipped_file in my_zip.namelist():
        local_name = local_name_prefix + zipped_file
        with open(local_name, "w"):  # clear file
            pass

        for line in my_zip.open(zipped_file).readlines():
            with open(local_name, "a") as f:
                f.write(line.decode())
