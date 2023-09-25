import requests
from zipfile import ZipFile
from io import BytesIO
from tqdm import tqdm

from Module.SqliteDriver import DB

import time  # add time.sleep(6) if query from nvdlib, due to requests rate limitation
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

    checked_set = set()  # set contains queried CVE
    checked_high_set = set()  # set contains CVE which above a threshold, (threshold default set to 7)

    cve_search = ares.CVESearch()
    for i in range(len(results)):
        record = results[i]
        cves = record[5].split(",")
        if contain_high_cve(cve_search, cves, checked_set, checked_high_set):
            potential_targets.update(record[2].split(","))
    return list(potential_targets)


def contain_high_cve(cve_search: ares.CVESearch, cves: list, checked_set: set, high_set: set, threshold: int = 7):
    for cve in tqdm(cves):
        if cve in checked_set:
            if cve in high_set:
                return True
            continue
        try:
            cve_info = cve_search.id(cve)
            cvss = cve_info["cvss"]
            checked_set.add(cve)
            if cvss and cvss > threshold:
                high_set.add(cve)
                return True
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Exception: {e} for CVE: {cve}")
        except requests.exceptions.ReadTimeout as e:
            print(f"Read Timeout: {e} when querying {cve}")
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
