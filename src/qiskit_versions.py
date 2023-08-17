import os
import requests
import json
from datetime import datetime

PACKAGE_NAME = "qiskit-terra"
VERSIONS_PATH = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "qiskit_versions.json"))

def get_qiskit_releases_data() -> dict:
    response = requests.get(f"https://pypi.org/pypi/{PACKAGE_NAME}/json")

    if response.status_code == 200:
        data = response.json()
        return data["releases"].items()
    return None

def get_qiskit_versions_info() -> []:
    data_items = get_qiskit_releases_data()

    # Temporary control dictionary for package release info for version, date and python version
    temp = {}

    # Filter data
    for release, release_info in data_items:
        # Skip RCs
        if "rc" in release:
            continue

        date_str = release_info[0]["upload_time"]
        date_format = "%Y-%m-%dT%H:%M:%S"
        date_time_obj = datetime.strptime(date_str, date_format)
        year = date_time_obj.year
        month = date_time_obj.month

        # Filter releases starting from 2020-03
        if (year == 2020 and month < 3) or year < 2020:
            continue

        python_version = release_info[0]["requires_python"]

        # Parse the release string of format "x.y.z" into a list of "x","y","z"
        major_minor_patch_list = release.split(".")
        major_minor = ".".join(major_minor_patch_list[:2])

        # Get latest patch
        patch_number = int(major_minor_patch_list[2])
        temp_info = temp.get(major_minor)
        previous_patch_number = -1 if not temp_info else temp_info[0]

        if previous_patch_number < patch_number:
            # Replace to latest patch version found
            temp[major_minor] = (patch_number, {"version":release, "date": date_str, "python_version": python_version})
            continue

    filtered_releases = []
    for _, value in temp.items():
        filtered_releases.append(value[1])

    return filtered_releases

def get_release_date(input_version:str) -> str:
    data_items = data_items = get_qiskit_releases_data()

    # Filter data
    for release, release_info in data_items:
        if release == input_version:
            # Remove time from date format "%Y-%m-%dT%H:%M:%S"
            date_time= release_info[0]["upload_time"]
            return date_time.split('T', 1)[0]
    return "Invalid version"

def write_versions_to_file(versions, filename=VERSIONS_PATH):
    with open(filename,"w") as file:
        json.dump(versions, file, indent=4)

# Uncomment lines alone to test this file output on its own
versions_info = get_qiskit_versions_info()
write_versions_to_file(versions_info)
# print(*versions_info, sep='\n')

"""
Qiskit Terra versions:
{'version': '0.13.0', 'date': '2020-04-09T21:22:39', 'python_version': '>=3.5'}
{'version': '0.14.2', 'date': '2020-06-15T21:02:04', 'python_version': '>=3.5'}
{'version': '0.15.2', 'date': '2020-09-08T18:01:48', 'python_version': '>=3.5'}
{'version': '0.16.4', 'date': '2021-02-08T17:16:48', 'python_version': '>=3.6'}
{'version': '0.17.4', 'date': '2021-05-18T21:24:27', 'python_version': '>=3.6'}
{'version': '0.18.3', 'date': '2021-09-29T11:57:07', 'python_version': '>=3.6'}
{'version': '0.19.2', 'date': '2022-02-02T14:03:42', 'python_version': '>=3.6'}
{'version': '0.20.2', 'date': '2022-05-18T15:29:49', 'python_version': '>=3.7'}
{'version': '0.21.2', 'date': '2022-08-23T21:07:29', 'python_version': '>=3.7'}
{'version': '0.22.4', 'date': '2023-01-17T13:01:47', 'python_version': '>=3.7'}
{'version': '0.23.3', 'date': '2023-03-21T19:16:16', 'python_version': '>=3.7'}
{'version': '0.24.2', 'date': '2023-07-19T18:23:22', 'python_version': '>=3.7'}
{'version': '0.25.0', 'date': '2023-07-27T22:01:11', 'python_version': '>=3.8'} => TODO: Update v0.25 results using this release
"""
