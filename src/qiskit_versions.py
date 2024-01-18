import os
import json
import qiskit
import requests
from datetime import datetime

def get_installed_version():
    try:
        # Starting with qiskit v0.45, qiskit and qiskit-terra will have the same version
        return qiskit.__version__
    except ImportError:
        return qiskit.__qiskit_version__["qiskit"]

def get_qiskit_releases_data(package_name: str) -> dict:
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    if response.status_code == 200:
        data = response.json()
        return data["releases"].items()
    return None

def get_qiskit_versions_info() -> []:
    data_items = get_qiskit_releases_data("qiskit")

    # Filter releases starting from 2023-11
    # Starting with qiskit 0.45, qiskit and qiskit-terra will have the same version
    return filter_by_date(data_items, [2023,11], [])

def get_qiskit_terra_versions_info() -> []:
    data_items = get_qiskit_releases_data("qiskit-terra")

    # Filter releases from 2020-03 (terra v0.13.x) to 2023-10 (terra v.0.25.x)
    return filter_by_date(data_items,[2020,3], [2023,10])

def get_qiskit_versions_list(package_name: str) -> []:
    qiskit_versions_info = get_qiskit_terra_versions_info() if "terra" in package_name else get_qiskit_versions_info()
    versions_only = []
    for item in qiskit_versions_info:
        for key, value in item.items():
            if key == "version":
                versions_only.append(value)
    return versions_only

def find_latest_version(versions: []) -> str:
  if not versions:
    return ""
  
  # Split each version string into a tuple of integers
  version_tuples = [tuple(map(int, v.split("."))) for v in versions]

  # Sort
  sorted_versions = sorted(version_tuples, reverse=True)

  # Convert the latest version tuple back to string
  latest_version = ".".join(map(str, sorted_versions[0]))
  return latest_version

# Compare versions in string format and return the highest
def compare_versions(version_1:str, version_2: str) -> str:
    # Split version strings into lists of ints
    # Split version strings into lists of ints
    v1_parts = list(map(int, version_1.split(".")))
    v2_parts = list(map(int, version_2.split(".")))

    # Compare
    for v1, v2 in zip(v1_parts, v2_parts):
        if v1 > int(v2):
            return version_1
        elif v1 < int(v2):
            return version_2
    return version_1 # if they are the same

def same_minor(version_1: str, version_2: str) -> bool:
    # Split version strings into lists of ints
    v1 = list(map(int, version_1.split(".")))
    v2 = list(map(int, version_2.split(".")))

    return v1[:2] == v2[:2]

def filter_by_date(data_items: dict, min_date: [], max_date: []) -> []:
    # Temporary control dictionary for package release info for version, date and python version
    temp = {}

    for release, release_info in data_items:

        # Skip RCs and pre-releases
        if "rc" in release or "b" in release:
            print("Skipping version ", release)
            continue
        
        date_str = release_info[0]["upload_time"]
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        year = dt.year
        month = dt.month

        if max_date:
            max_y, max_m = max_date
            # Ignore above max_date
            if (year == max_y and month > max_m) or year > max_y:
                continue
    
        min_y, min_m = min_date
        # Ignore below min_date
        if (year == min_y and month < min_m) or year < min_y:
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

def get_qiskit_version_map_history():
    version_map = {}
    
    return version_map

###
# qiskit_info = get_qiskit_versions_info()
# print("qiskit versions:", sep='\n')
# print(*qiskit_info, sep='\n')
"""
qiskit versions:
{'version': '0.45.0', 'date': '2023-11-03', 'python_version': '>=3.8'}
"""

# qiskit_terra_info = get_qiskit_terra_versions_info()
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
{'version': '0.25.3', 'date': '2023-10-25', 'python_version': '>=3.8'}
"""

###
# version_history_map = get_qiskit_version_map_history()

# def markdown_table_to_csv(md_file_path: str, csv_file_path: str):

# Use qiskit version history map to rename all result filenames
md_file_path = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "qiskit_releases.md"))
csv_file_path = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "qiskit_releases.csv"))
# markdown_table_to_csv(md_file_path, csv_file_path)
