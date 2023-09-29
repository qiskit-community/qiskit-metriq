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

ARCHITECTURES = ["ibm_rochester", "rigetti_16q_aspen"]
CONTENT_URL = "https://github.com/qiskit-community/qiskit-metriq"
METRICS = ["Circuit depth", "Gate count"]
METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")
RESULTS_PATH = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "results"))
THUMBNAIL_URL = "https://avatars.githubusercontent.com/u/30696987?s=200&v=4"

# Metriq API parameters and associated ids
METHOD = {"8": "Qiskit compilation"}
PLATFORMS = {"64": "Rigetti 16Q Aspen-1 ", "69": "ibmq-rochester"}
TAGS = ["quantum circuits", "compiler", "compilation", "ibm qiskit"]
TASKS = {"25": "ex1_226.qasm", "26": "ex1_226.qasm (Aspen)", "27": "ex1_226.qasm (Rochester)"}
SUBMISSIONS = {"595": TASKS["25"],"661": TASKS["26"], "662": TASKS["27"]}

def get_substring_between_parentheses(input_str: str) -> str:
  start = input_str.find("(")
  end = input_str.find(")")
  if start != -1 and end != -1:
    substring = input_str[start +1: end]
    return substring
  else:
    return None

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

def files_to_be_processed (submission_id: str) -> []:
  all_filenames = os.listdir(RESULTS_PATH)
  files_to_processed = []
  for filename in all_filenames:
    if VERSION in filename:
      if submission_id == "595":
        files_to_processed.append(filename)
      else:
        # Filter filenames matching architecture
        task_name = SUBMISSIONS[submission_id].lower()
        for arch in ["aspen", "rochester"]:
          if arch in task_name and arch in filename:
              files_to_processed.append(filename)
  return files_to_processed

def submit(client: MetriqClient, submission_id: str):
  filenames = files_to_be_processed(submission_id)
  for filename in filenames:
    # Process results and add them to existing submission
    file_path = os.path.join(RESULTS_PATH, f"{filename}")
    df = pd.read_csv(file_path, sep='|')
    task_id = get_id(TASKS, SUBMISSIONS[submission_id])
    method_id = get_id(METHOD, "Qiskit compilation")
    process_results(df, client, task_id, method_id, submission_id)

def submit_all(client: MetriqClient, task_name: str, submission_id: str = None):
  if not submission_id:
    submission_id = create_new_submission(client,task_name)
  
  # Process results
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

def create_new_submission(client: MetriqClient, task_name: str) -> str:
  submission_req = SubmissionCreateRequest()
  submission_req.name = task_name
  submission_req.contentUrl = CONTENT_URL
  submission_req.thumbnailUrl = THUMBNAIL_URL
  submission_req.description = f"Qiskit compilation for {task_name} benchmark circuit"
  submission_req.codeUrl = CONTENT_URL
  platform_keyword = get_substring_between_parentheses(task_name)
  platform_id = get_platform_id(platform_keyword)
  submission_req.platform = platform_id

  submission_id = client.submission_add(submission_req)["id"]
  # Populate other submission parameters
  # Task
  client.submission_add_task(submission_id, get_id(TASKS, task_name))
  # Method
  client.submission_add_method(submission_id, get_id(METHOD, "Qiskit compilation"))
  # Tags
  for tag in TAGS:
    client.submission_add_tag(submission_id, tag)
  return submission_id

def process_results(dataframe, client: MetriqClient, task_id: str, method_id: str, submission_id: str):
  for metric in METRICS:
    result_item = ResultCreateRequest()
    result_item.task = task_id # Must be id
    result_item.method = method_id # Must be id
    result_item.metricName = metric
    result_item.metricValue = str(round(dataframe[metric].mean(),3)) # Must be a string
    result_item.evaluatedAt = dataframe["Date"].iloc[0]
    result_item.isHigherBetter = "false"

    platform_name = dataframe["Platform"].iloc[0] # This is not an exact match with metriq platform names
    # Get last word and find it in PLATFORMS
    platform_keyword = platform_name.rsplit('_', 1)[-1]
    platform_id = get_platform_id(platform_keyword)
    result_item.platform = platform_id # Must be id

    sample_size = len(dataframe.index)
    result_item.sampleSize = sample_size
    std_err = dataframe[metric].sem()
    result_item.standardError = str(round(std_err, 3)) # Must be a string

    # Get extra info and add to notes
    metric_std = dataframe[metric].std()
    opt_level = dataframe["Opt level"].iloc[0]
    version = dataframe["Method"].iloc[0].split(" ")[1] # Must be same as VERSION
    package_name = "qiskit" if VERSION == compare_versions(VERSION, "0.25.0") else "qiskit-terra"
    result_item.notes = f"Stdev: {round(metric_std,3)}, Optimization level:{opt_level}, {package_name} version:{version}"

    client.result_add(result_item, submission_id)

def evaluate_metrics(qiskit_version: str) -> dict:
  processed_summary = {}

  # Process results and save to file
  filenames = os.listdir(RESULTS_PATH)
  for filename in filenames:
    if qiskit_version in filename:
      for arch in ARCHITECTURES:
        if arch in filename:
          file_path = os.path.join(RESULTS_PATH, f"{filename}")
          df = pd.read_csv(file_path, sep='|')
          obj_key = qiskit_version + "-" + arch
          processed_summary[obj_key] = []
          
          for metric in METRICS:
            col = df[metric]
            mean = col.mean()
            stdev = col.std()
            stderr = col.sem()

            processed_summary[obj_key].append(
              {metric: 
                {"ave": mean, 
                "stdev": round(stdev,3), 
                "stderr": round(stderr,3)}
              })
  return processed_summary

def append_to_json_file(json_file_path, processed_info):
  try:
    with open(json_file_path, "r") as f:
      data = json.load(f)
  except json.JSONDecodeError:
      data = []
  data.append(processed_info)
  with open(json_file_path, "w") as f:
    json.dump(data, f, indent=4)

def create_processed_data_summary():
  versions_info = get_qiskit_versions_info()
  for info in versions_info:
      qiskit_version = info["version"]
      processed_summary = evaluate_metrics(qiskit_version)
      json_file_path = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "processed_data_summary.json"))
      append_to_json_file(json_file_path, processed_summary)

# create_processed_data_summary()

submission_id = os.getenv("SUBMISSION_ID")
print(f"Processing submission {submission_id}...")
client = MetriqClient(token=METRIQ_TOKEN)
submit(client, submission_id)

