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
# versions_info = get_qiskit_versions_info()
# write_versions_to_file(versions_info)
# print(*versions_info, sep='\n')