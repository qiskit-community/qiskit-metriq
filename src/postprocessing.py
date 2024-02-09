import os
import json
import pandas as pd
from metriq import MetriqClient
from metriq.models.result import ResultCreateRequest
from metriq.models.submission import SubmissionCreateRequest
from qiskit_versions import *

VERSION = get_installed_version()
ARCHITECTURES = ["ibm_rochester", "rigetti_16q_aspen"]
CONTENT_URL = "https://github.com/qiskit-community/qiskit-metriq"
METRICS = ["Circuit depth", "Gate count"]
METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")
RESULTS_PATH = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "results"))
SUMMARY_PATH = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "processed_data_summary.json"))
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
  print("Processing results for Qiskit version ", VERSION)
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

    # Get extra info and add to notes
    metric_std = dataframe[metric].std()
    opt_level = dataframe["Opt level"].iloc[0]
    version = dataframe["Method"].iloc[0].split(" ")[1] # Must be same as VERSION
    package_name = "qiskit" if VERSION == compare_versions(VERSION, "0.25.3") else "qiskit-terra"
    result_item.notes = f"Stdev: {round(metric_std,3)}, Optimization level:{opt_level}, {package_name} version:{version}"

    # TODO: Need to add sample size and std err manually
    # sample_size = len(dataframe.index)
    # result_item.sampleSize = sample_size #ValueError: "ResultCreateRequest" object has no field "sampleSize"
    # std_err = dataframe[metric].sem()
    # result_item.standardError = str(round(std_err, 3)) # Must be a string #ValueError: "ResultCreateRequest" object has no field "standardError"

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

def append_to_json_file(json_file_path: str, processed_info: dict, version: str):
  try:
    with open(json_file_path, "r") as f:
      data = json.load(f)
      # Convert the JSON data to a string
      json_string = json.dumps(data)
  except json.JSONDecodeError:
      data = []
      json_string = ""

  # Only write to file if version is not in file
  if version not in json_string:
    data.append(processed_info)
    with open(json_file_path, "w") as f:
      json.dump(data, f, indent=4)
    print(f"Summary for version '{version}' added to file.")
  else:
    print(f"Summary for version '{version}' is already in file.")

def create_processed_data_summary():
  submitted_q_versions = ["0.45.2","0.44.3","0.42.1","0.39.5","0.37.2","0.36.2","0.34.2","0.30.1","0.26.1","0.23.5","0.20.1","19.4","0.18.0"]
  submitted_q_versions.reverse()
  for qiskit_version in submitted_q_versions:
    processed_summary = evaluate_metrics(qiskit_version)
    append_to_json_file(SUMMARY_PATH, processed_summary, qiskit_version)

# create_processed_data_summary()

# Process data
processed_summary = evaluate_metrics(VERSION)
append_to_json_file(SUMMARY_PATH, processed_summary, VERSION)

# Submit to Metriq.info
submission_id = os.getenv("SUBMISSION_ID")
print(f"Processing submission {submission_id}...")
client = MetriqClient(token=METRIQ_TOKEN)
submit(client, submission_id)