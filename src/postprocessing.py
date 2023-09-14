import os
import pandas as pd
from metriq import MetriqClient
from metriq.models.result import ResultCreateRequest
from metriq.models.submission import (Submission, SubmissionCreateRequest)
from preprocessing import get_submission_results
from qiskit_versions import compare_versions
try:
  # Try to import qiskit version from 0.44.0 and above
  from qiskit import __qiskit_version__
  VERSION = __qiskit_version__["qiskit"]
except ImportError:
  # Import from older versions
  import qiskit
  VERSION = qiskit.__version__

METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")
RESULTS_PATH = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "results"))
CONTENT_URL = "https://github.com/qiskit-community/qiskit-metriq"
THUMBNAIL_URL = "https://avatars.githubusercontent.com/u/30696987?s=200&v=4"

# Metriq API parameters and associated ids
METHOD = {"8": "Qiskit compilation"}
PLATFORMS = {"64": "Rigetti 16Q Aspen-1 ", "69": "ibmq-rochester"}
TAGS = ["quantum circuits", "compiler", "compilation", "ibm qiskit"]
TASKS = {"25": "ex1_226.qasm", "26": "ex1_226.qasm (Aspen)", "27": "ex1_226.qasm (Rochester)"}
SUBMISSIONS = {"595": TASKS["25"],"661": TASKS["26"], "662": TASKS["27"]}

def get_id(input_list: dict, input_value: str) -> str:
  # Return key from value
  return list(input_list.keys())[list(input_list.values()).index(input_value)]

def get_platform_id(keywork: str) -> str:
  norm_keyword = keywork.lower()
  for key, value in PLATFORMS.items():
    norm_value = value.lower()
    if norm_keyword in norm_value:
      return key
  return None

def submit(client: MetriqClient, qiskit_version:str, task_name: str, submission_id: str):
  # Process results and add them to submission
  filenames = os.listdir(RESULTS_PATH)
  for filename in filenames:
    if qiskit_version in filename:
      # TODO handle task 25 case - ignore architecture and process all
      for arch in ["aspen", "rochester"]:
        if arch in filename and arch in task_name.lower():
          file_path = os.path.join(RESULTS_PATH, f"{filename}")
          df = pd.read_csv(file_path, sep='|')
          task_id = get_id(TASKS, task_name)
          method_id = get_id(METHOD, "Qiskit compilation")
          process_results(df, client, task_id, method_id, submission_id)

def submit_all(client: MetriqClient, task_name: str, submission_id: str = None):
  if not submission_id:
    create_new_submission(client,task_name)
  
  # TODO handle code duplication with submit()
  # Process results and add them to submission
  filenames = os.listdir(RESULTS_PATH)
  for filename in filenames:
    architectures = ["aspen", "rochester"]
    for arch in architectures:
      if arch in filename and arch in task_name.lower():
        print(f"*** Processing {arch} results from {filename}")
        file_path = os.path.join(RESULTS_PATH, f"{filename}")
        df = pd.read_csv(file_path, sep='|')
        task_id = get_id(TASKS, task_name)
        method_id = get_id(METHOD, "Qiskit compilation")
        process_results(df, client, task_id, method_id, submission_id)

def create_new_submission(client: MetriqClient, task_name: str):
  submission_req = SubmissionCreateRequest()
  submission_req.name = task_name
  submission_req.contentUrl = CONTENT_URL
  submission_req.thumbnailUrl = THUMBNAIL_URL
  submission_req.description = f"Qiskit compilation for {task_name} benchmark circuit"
  client.submission_add(submission_req)
  # Populate other submission parameters
  # Task
  client.submission_add_task(submission_id, get_id(TASKS, task_name))
  # Method
  client.submission_add_method(submission_id, get_id(METHOD, "Qiskit compilation"))
  # Tags
  for tag in TAGS:
    client.submission_add_tag(submission_id, tag)
  # TODO Update params below using the API - currently not supported
  # submission.codeUrl
  # submission.platform

def process_results(dataframe, client: MetriqClient, task_id: str, method_id: str, submission_id: str):
  metrics = ["Circuit depth", "Gate count"]
  for metric in metrics:
    result_item = ResultCreateRequest()
    result_item.task = task_id # Must be id
    result_item.method = method_id # Must be id
    result_item.metricName = metric
    result_item.metricValue = str(round(dataframe[metric].mean())) # Must be a string
    result_item.evaluatedAt = dataframe["Date"].iloc[0]
    result_item.isHigherBetter = "false"

    platform_name = dataframe["Platform"].iloc[0] # This is not an exact match with metriq platform names
    # Get last word and find it in PLATFORMS
    platform_keyword = platform_name.rsplit('_', 1)[-1]
    platform_id = get_platform_id(platform_keyword)
    result_item.platform = platform_id # Must be id

    # TODO: Update sample size - currently not supported
    # sample_size = len(dataframe.index)
    # result_item.sampleSize = sample_size # ERROR: object has no field "sampleSize"

    # Get extra info and add to notes
    metric_std = dataframe[metric].std()
    opt_level = dataframe["Opt level"].iloc[0]
    version = dataframe["Method"].iloc[0].split(" ")[1] # Must be same as VERSION
    package_name = "qiskit" if VERSION == compare_versions(VERSION, "0.25.0") else "qiskit-terra"
    result_item.notes = f"Stdev: {round(metric_std,3)}, Optimization level:{opt_level}, {package_name} version:{version}"

    client.result_add(result_item, submission_id)

submission_id = os.getenv("SUBMISSION_ID")
print(f"Processing submission {submission_id}...")
client = MetriqClient(token=METRIQ_TOKEN)
submit(client, VERSION, SUBMISSIONS[submission_id], submission_id)