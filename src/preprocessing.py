
import os
from metriq import MetriqClient
from qiskit_versions import get_qiskit_versions_info

METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")
TASKS = {"25": "ex1_226.qasm", "26": "ex1_226.qasm (Aspen)", "27": "ex1_226.qasm (Rochester)"}
SUBMISSIONS = {"595": TASKS["25"],"661": TASKS["26"], "662": TASKS["27"]}

'''
Pre-processing steps:
1. Fetch qiskit versions
2. Fetch metriq results
3. Compare 1. and 2. and find missing versions to be executed and uploaded
4. Decide if new result needs to be uploaded or replace an existing
'''

def get_id(param_list: dict, param_name: str) -> str:
  # Return key from value
  return list(param_list.keys())[list(param_list.values()).index(param_name)]

def get_submission_results(client: MetriqClient, submission_id: str) -> []:
  return client.http.get(f"/submission/{submission_id}/")["data"]["results"]
  # return client.submission_get(submission_id)

def get_qiskit_version_from_result(result_item: dict) -> str:
  notes = result_item["notes"]
  # Notes have extra info in the format "Stdev: f, Optimization level:i, qiskit-terra version:x.y.z"
  # Get substring after last colon
  return notes.rsplit(":", 1)[1]

# 1. Fetch qiskit versions
qiskit_versions_data = get_qiskit_versions_info()
print("qiskit_versions_data:")
print(qiskit_versions_data)

# 2. Fetch metriq results
client = MetriqClient(token=METRIQ_TOKEN)
submission_ids = list(SUBMISSIONS.keys())
qiskit_versions_submitted = {}

for submission_id in submission_ids:
  results = get_submission_results(client, submission_id)
  submissions = []
  for res in results:
    submissions.append(get_qiskit_version_from_result(res))
  qiskit_versions_submitted[submission_id] = submissions

print("qiskit_versions_submitted: ")
for key, value in qiskit_versions_submitted.items():
  print(key, ": ", value)

# 3. Compare 1. and 2. and find missing versions to be executed and uploaded
for v_data in qiskit_versions_data:
  version = v_data["version"]
  for key, value in qiskit_versions_submitted.items():
    if version in value:
      print(f"Version {version} is in submission {key}")
    else:
      print(f"Version {version} is not in submission {key}")
