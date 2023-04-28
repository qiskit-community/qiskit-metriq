import requests
import json
from datetime import datetime, timedelta

response = requests.get("https://pypi.org/pypi/qiskit-terra/json")
data = response.json()
data_items = data["releases"].items()

# Store an array of filtered_releases, which is a list of
# objects containing relevant info of each package release, such as:
# version, date, python version
#TODO:
# Add python version info for each release
filtered_releases = []

# Filter data
for release, release_info in data_items:
    date_str = release_info[0]["upload_time"]
    filtered_release_info = {"version":release, "date": date_str}

    # TODO: refactor loop logic to look nicer
    # Skip RCs and patch versions
    if "rc" not in release:
        # Skip patch versions
        patch_number = int(release.split(".")[2])
        patch = patch_number > 0
        if not patch:
            filtered_release_info = {"version":release, "date": date_str}

            # Filter releases starting from 2020-03
            date_format = "%Y-%m-%dT%H:%M:%S"
            date_time_obj = datetime.strptime(date_str, date_format)
            year = date_time_obj.year
            month = date_time_obj.month

            if year == 2020 and month > 3 or year > 2020:
                filtered_releases.append(filtered_release_info)

print('Qiskit Terra versions')
print(*filtered_releases, sep='\n')

    