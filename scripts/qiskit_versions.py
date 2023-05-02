import requests
import json
from datetime import datetime, timedelta

response = requests.get("https://pypi.org/pypi/qiskit-terra/json")
data = response.json()
data_items = data["releases"].items()
python_version = "3.7"
# Since Python 3.6 and below have reached end of life
# Using 3.7 here as it is compatible with all qiskit-terra versions

# List of objects containing relevant info of each package release, such as:
# version, date, python version
filtered_releases = []

# Filter data
for release, release_info in data_items:
    date_str = release_info[0]["upload_time"]
    # python_version = release_info[0]["requires_python"]

    # TODO: maybe refactor loop logic to look nicer
    # Skip RCs and patch versions
    if "rc" not in release:
        # Skip patch versions
        patch_number = int(release.split(".")[2])
        patch = patch_number > 0
        if not patch:
            filtered_release_info = {"version":release, "date": date_str, "python_version": python_version}
            # , "python_version": python_version}

            # Filter releases starting from 2020-03
            date_format = "%Y-%m-%dT%H:%M:%S"
            date_time_obj = datetime.strptime(date_str, date_format)
            year = date_time_obj.year
            month = date_time_obj.month

            if year == 2020 and month > 3 or year > 2020:
                filtered_releases.append(filtered_release_info)

print('Qiskit Terra versions: \n')
print(*filtered_releases, sep='\n')

"""
Filtered data output example

$ python scripts/qiskit_versions.py
Qiskit Terra versions
{'version': '0.13.0', 'date': '2020-04-09T21:22:39', 'python_version': '>=3.5'}
{'version': '0.14.0', 'date': '2020-04-30T20:52:56', 'python_version': '>=3.5'}
{'version': '0.15.0', 'date': '2020-08-06T18:02:45', 'python_version': '>=3.5'}
{'version': '0.16.0', 'date': '2020-10-15T21:31:06', 'python_version': '>=3.6'}
{'version': '0.17.0', 'date': '2021-04-01T15:51:06', 'python_version': '>=3.6'}
{'version': '0.18.0', 'date': '2021-07-12T19:41:19', 'python_version': '>=3.6'}
{'version': '0.19.0', 'date': '2021-12-06T20:03:48', 'python_version': '>=3.6'}
{'version': '0.20.0', 'date': '2022-03-31T21:05:16', 'python_version': '>=3.7'}
{'version': '0.21.0', 'date': '2022-06-30T17:16:08', 'python_version': '>=3.7'}
{'version': '0.22.0', 'date': '2022-10-13T19:23:19', 'python_version': '>=3.7'}
{'version': '0.23.0', 'date': '2023-01-26T22:07:35', 'python_version': '>=3.7'}

Example of extra python version info
{'version': '0.13.0', 'date': '2020-04-09T21:22:39', 'requires_python': '>=3.5', 'python_version': 'cp35'}
{'version': '0.14.0', 'date': '2020-04-30T20:52:56', 'requires_python': '>=3.5', 'python_version': 'cp35'}
{'version': '0.15.0', 'date': '2020-08-06T18:02:45', 'requires_python': '>=3.5', 'python_version': 'cp35'}
{'version': '0.16.0', 'date': '2020-10-15T21:31:06', 'requires_python': '>=3.6', 'python_version': 'cp36'}
{'version': '0.17.0', 'date': '2021-04-01T15:51:06', 'requires_python': '>=3.6', 'python_version': 'cp36'}
{'version': '0.18.0', 'date': '2021-07-12T19:41:19', 'requires_python': '>=3.6', 'python_version': 'cp36'}
{'version': '0.19.0', 'date': '2021-12-06T20:03:48', 'requires_python': '>=3.6', 'python_version': 'cp36'}
{'version': '0.20.0', 'date': '2022-03-31T21:05:16', 'requires_python': '>=3.7', 'python_version': 'cp310'}
{'version': '0.21.0', 'date': '2022-06-30T17:16:08', 'requires_python': '>=3.7', 'python_version': 'cp310'}
{'version': '0.22.0', 'date': '2022-10-13T19:23:19', 'requires_python': '>=3.7', 'python_version': 'cp310'}
{'version': '0.23.0', 'date': '2023-01-26T22:07:35', 'requires_python': '>=3.7', 'python_version': 'cp310'}
"""
