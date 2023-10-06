import os
from metriq import MetriqClient
from qiskit_versions import *

METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")
TASKS = {"25": "ex1_226.qasm", "26": "ex1_226.qasm (Aspen)", "27": "ex1_226.qasm (Rochester)"}
SUBMISSIONS = {"595": TASKS["25"],"661": TASKS["26"], "662": TASKS["27"]}

def get_submission_results(client: MetriqClient, submission_id: str) -> []:
  return client.http.get(f"/submission/{submission_id}/")["data"]["results"]
  # return client.submission_get(submission_id)

def get_qiskit_version_from_result(result_item: dict) -> str:
  notes = result_item["notes"]
  # Notes have extra info in the format "Stdev: f, Optimization level:i, qiskit-terra version:x.y.z"
  # Get substring after last colon
  return notes.rsplit(":", 1)[1]

def get_submissions_update_info() -> {}:
  # Fetch latest qiskit version
  latest_qiskit_version = find_latest_version(get_qiskit_versions_list())

  # Fetch metriq results
  client = MetriqClient(token=METRIQ_TOKEN)
  submission_ids = list(SUBMISSIONS.keys())

  # For each metriq submission, keep track of qiskit versions submitted
  qiskit_versions_submitted = {}
  for submission_id in submission_ids:
    results = get_submission_results(client, submission_id)
    submissions = []
    for res in results:
      submissions.append(get_qiskit_version_from_result(res))
    qiskit_versions_submitted[submission_id] = submissions

  submissions_update_info = {}

  # Find new qiskit versions to be either added or replaced in metriq
  for key, value in qiskit_versions_submitted.items():
    latest_submitted_version = find_latest_version(value)
    versions_to_be_added = []
    versions_to_be_replaced = []

    if latest_qiskit_version == latest_submitted_version:
      # submission is up to date
      continue

    if latest_qiskit_version == compare_versions(latest_qiskit_version, latest_submitted_version):
      versions_to_be_added.append(latest_qiskit_version)
      if same_minor(latest_qiskit_version, latest_submitted_version):
        versions_to_be_replaced.append(latest_submitted_version)  

    submissions_update_info[key] = {"add": versions_to_be_added, "replace": versions_to_be_replaced}
  
  return submissions_update_info

def delete_submission_results(submission_id: str, qiskit_version: str):
  client = MetriqClient(token=METRIQ_TOKEN)
  results = get_submission_results(client, submission_id)

  # Find results items linked to qiskit_version
  for res in results:
    notes = res["notes"]
    if qiskit_version in notes:
      result_id = res["id"]
      # Delete result from submission
      print(f"Deleting qiskit version {qiskit_version} result from submission {submission_id}...")
      client.http.delete(f"/result/{result_id}/")


