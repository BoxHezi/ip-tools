import requests
import pprint

from zipfile import ZipFile
from io import BytesIO


# NIST NVD CVE API reference: https://nvd.nist.gov/developers/vulnerabilities
# NVDLib Documentation: https://nvdlib.com/en/latest/v1/v1.html#search-cpe

# CAPEC CSV: https://capec.mitre.org/data/csv/2000.csv.zip
# CWE CSV: https://cwe.mitre.org/data/csv/2000.csv.zip

def search_cve(cve_id: str):
    # CIRCL_BASE_URL = "https://cve.circl.lu/api/cve/"
    # NIST_NVD_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    # url = CIRCL_BASE_URL + cve_id
    # resp = requests.get(url).json()
    # pprint.pprint(resp)
    download_file("https://capec.mitre.org/data/csv/2000.csv.zip", "capec")
    download_file("https://cwe.mitre.org/data/csv/2000.csv.zip", "cwe")


def search_cpe(cpe_name: str):
    pass


def download_file(url: str, prefix: str):
    local_name_prefix = "./databases/" + prefix
    resp = requests.get(url)
    my_zip = ZipFile(BytesIO(resp.content))

    for zipped in my_zip.namelist():
        local_name = local_name_prefix + zipped
        with open(local_name, "w"):  # clear file
            pass

        for line in my_zip.open(zipped).readlines():
            with open(local_name, "a") as f:
                f.write(line.decode())
