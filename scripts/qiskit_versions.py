import requests
import json
from datetime import datetime, timedelta

response = requests.get("https://pypi.org/pypi/qiskit-terra/json")
data = response.json()
data_items = data["releases"].items()

# TODO:
# Remove RCs and patch versions
for release, release_info in data_items:
    date_str = release_info[0]["upload_time"]

    # Transform date string into time object 
    date_format = "%Y-%m-%dT%H:%M:%S"
    date_time_obj = datetime.strptime(date_str, date_format)

    # Get the relevant time pieces
    year = date_time_obj.year
    month = date_time_obj.month

    # Filter releases starting from 2020-03
    valid_release_info = ""
    if year == 2020:
        if month > 3:
            valid_release_info = f"{release}{' from '}{year}{'-'}{month}"
            print(valid_release_info)
    if year > 2020:
        valid_release_info = f"{release}{' from '}{year}{'-'}{month}"
        print(valid_release_info)



    