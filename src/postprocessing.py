
import os
import pandas as pd
from metriq import MetriqClient
from metriq.models.result import ResultCreateRequest
from metriq.models.submission import (Submission, SubmissionCreateRequest)
from qiskit_versions import *

METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")
RESULTS_PATH = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "results"))
ARCHITECTURES = ["ibm_rochester", "rigetti_16q_aspen"]
CONTENT_URL = "https://github.com/qiskit-community/qiskit-metriq"
THUMBNAIL_URL = "https://avatars.githubusercontent.com/u/30696987?s=200&v=4"

# Metriq API parameters and associated ids
METHOD = {"8": "Qiskit compilation"}
PLATFORMS = {"64": "Rigetti 16Q Aspen-1 ", "69": "ibmq-rochester"}
TAGS = ["quantum circuits", "compiler", "compilation", "ibm qiskit"]
TASKS = {"25": "ex1_226.qasm", "26": "ex1_226.qasm (Aspen)", "27": "ex1_226.qasm (Rochester)"}

def get_substring_between_parentheses(input_str: str) -> str:
  start = input_str.find("(")
  end = input_str.find(")")
  if start != -1 and end != -1:
    substring = input_str[start +1: end]
    return substring
  else:
    return None

def get_id(param_list: dict, param_name: str) -> str:
  # Return key from value
  return list(param_list.keys())[list(param_list.values()).index(param_name)]

def get_platform_id(keywork: str) -> str:
  norm_keyword = keywork.lower()
  for key, value in PLATFORMS.items():
    norm_value = value.lower()
    if norm_keyword in norm_value:
      return key
  return None

# TODO Keep track of results already submitted and prepare automation pipeline
def submit_all(task_name: str, submission_id: str = None):
  client = MetriqClient(token=METRIQ_TOKEN)

  if not submission_id:
    create_new_submission(client,task_name)

  # Populate submission parameters
  # Task
  task_id = get_id(TASKS, task_name)
  client.submission_add_task(submission_id, task_id)

  # Method
  method_id = get_id(METHOD, "Qiskit compilation")
  client.submission_add_method(submission_id, method_id)

  # Tags
  for tag in TAGS:
    client.submission_add_tag(submission_id, tag)
  
  # Process results and add them to submission
  filenames = os.listdir(RESULTS_PATH)
  for filename in filenames:
    architectures = ["aspen", "rochester"]
    for arch in architectures:
      if arch in filename and arch in task_name.lower():
        print(f"*** Processing {arch} results from {filename}")
        file_path = os.path.join(RESULTS_PATH, f"{filename}")
        df = pd.read_csv(file_path, sep='|')
        process_results(df, client, task_id, method_id, submission_id)

def create_new_submission(client: MetriqClient, task_name: str):
  submission_req = SubmissionCreateRequest()
  submission_req.name = task_name
  submission_req.contentUrl = CONTENT_URL
  submission_req.thumbnailUrl = THUMBNAIL_URL
  submission_req.description = f"Qiskit compilation for {task_name} benchmark circuit"
  submission_req.codeUrl = CONTENT_URL
  platform_keyword = get_substring_between_parentheses(task_name)
  platform_id = get_platform_id(platform_keyword)
  submission_req.platform = platform_id
  client.submission_add(submission_req)

def process_results(dataframe, client: MetriqClient, task_id: str, method_id: str, submission_id: str):
  metrics = ["Circuit depth", "Gate count"]
  for metric in metrics:
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
    version = dataframe["Method"].iloc[0].split(" ")[1]
    result_item.notes = f"Stdev: {round(metric_std,3)}, Optimization level:{opt_level}, qiskit-terra version:{version}"

    client.result_add(result_item, submission_id)

def evaluate_metrics(qiskit_version: str) -> dict:
  metrics = ["Circuit depth", "Gate count"]
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
          
          for metric in metrics:
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

# TODO Get submission ids from client
# submit_all(TASKS["26"], "661")
# submit_all(TASKS["27"], "662")
