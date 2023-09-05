import os
import requests
import json
from datetime import datetime

def get_qiskit_releases_data(package_name: str) -> dict:
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    if response.status_code == 200:
        data = response.json()
        return data["releases"].items()
    return None

def get_qiskit_versions_info() -> []:
    data_items = get_qiskit_releases_data("qiskit")

    # Filter releases starting from 2023-08
    # Starting with qiskit 0.45, qiskit and qiskit-terra will have the same version
    return filter_by_date(data_items,2023,8)

def get_qiskit_terra_versions_info() -> []:
    data_items = get_qiskit_releases_data("qiskit-terra")

    # Filter releases starting from 2020-03 (qiskit-terra version 0.13.0)
    return filter_by_date(data_items,2020,3)

def filter_by_date(data_items: dict, y: int, m: int) -> []:
    # Temporary control dictionary for package release info for version, date and python version
    temp = {}

    for release, release_info in data_items:
        # Skip RCs
        if "rc" in release:
            continue

        date_str = release_info[0]["upload_time"]
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        year = dt.year
        month = dt.month
        
        if (year == y and month < m) or year < y:
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
            temp[major_minor] = (patch_number, {"version":release, "date": dt.strftime("%Y-%m-%d"), "python_version": python_version})
            continue

    filtered_releases = []
    for _, value in temp.items():
        filtered_releases.append(value[1])

    return filtered_releases

def write_versions_to_file(versions: [], filename: str):
    file_path = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", filename))
    with open(file_path,"w") as file:
        json.dump(versions, file, indent=4)

def get_version_date(package_name: str, input_version:str) -> str:
    data_items = data_items = get_qiskit_releases_data(package_name)
    for release, release_info in data_items:
        if release == input_version:
            # Remove time from date format "%Y-%m-%dT%H:%M:%S"
            date_time= release_info[0]["upload_time"]
            return date_time.split('T', 1)[0]
    return "Invalid version"

qiskit_info = get_qiskit_versions_info()
# write_versions_to_file(qiskit_info, "qiskit.json")
print("qiskit versions:", sep='\n')
print(*qiskit_info, sep='\n')
"""
qiskit versions:
{'version': '0.44.1', 'date': '2023-08-17', 'python_version': '>=3.8'}
"""

# NOTE: qiskit-terra package used up until Aug 2023. Future experiment runs to use qiskit package only.
# qiskit_terra_info = get_qiskit_terra_versions_info()
# write_versions_to_file(qiskit_terra_info, "qiskit_versions.json")
# print("qiskit-terra versions:", sep='\n')
# print(*qiskit_terra_info, sep='\n')
"""
qiskit-terra versions:
{'version': '0.13.0', 'date': '2020-04-09', 'python_version': '>=3.5'}
{'version': '0.14.2', 'date': '2020-06-15', 'python_version': '>=3.5'}
{'version': '0.15.2', 'date': '2020-09-08', 'python_version': '>=3.5'}
{'version': '0.16.4', 'date': '2021-02-08', 'python_version': '>=3.6'}
{'version': '0.17.4', 'date': '2021-05-18', 'python_version': '>=3.6'}
{'version': '0.18.3', 'date': '2021-09-29', 'python_version': '>=3.6'}
{'version': '0.19.2', 'date': '2022-02-02', 'python_version': '>=3.6'}
{'version': '0.20.2', 'date': '2022-05-18', 'python_version': '>=3.7'}
{'version': '0.21.2', 'date': '2022-08-23', 'python_version': '>=3.7'}
{'version': '0.22.4', 'date': '2023-01-17', 'python_version': '>=3.7'}
{'version': '0.23.3', 'date': '2023-03-21', 'python_version': '>=3.7'}
{'version': '0.24.2', 'date': '2023-07-19', 'python_version': '>=3.7'}
{'version': '0.25.1', 'date': '2023-08-17', 'python_version': '>=3.8'}
"""
