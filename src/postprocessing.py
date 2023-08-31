
import os
import pandas as pd
from metriq import MetriqClient
from metriq.models.result import ResultCreateRequest
from metriq.models.submission import (Submission, SubmissionCreateRequest)

METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")
RESULTS_PATH = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "results"))

CONTENT_URL = "https://github.com/qiskit-community/submit-metriq"
THUMBNAIL_URL = "https://avatars.githubusercontent.com/u/30696987?s=200&v=4"

# Metriq API parameters and associated ids
METHOD = {"8": "Qiskit compilation"}
PLATFORMS = {"64": "Rigetti 16Q Aspen-1 ", "69": "ibmq-rochester"}
TAGS = ["quantum circuits", "compiler", "compilation", "ibm qiskit"]
TASKS = {"25": "ex1_226.qasm", "26": "ex1_226.qasm (Aspen)", "27": "ex1_226.qasm (Rochester)"}

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

  # TODO Find a way to to update params below using the API
  # submission.codeUrl
  # submission.platform
  
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
  client.submission_add(submission_req)

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

    # TODO: Update sample size
    # sample_size = len(dataframe.index)
    # result_item.sampleSize = sample_size # ERROR: object has no field "sampleSize"

    # Get extra info and add to notes
    metric_std = dataframe[metric].std()
    opt_level = dataframe["Opt level"].iloc[0]
    version = dataframe["Method"].iloc[0].split(" ")[1]
    result_item.notes = f"Stdev: {round(metric_std,3)}, Optimization level:{opt_level}, qiskit-terra version:{version}"

    client.result_add(result_item, submission_id)

# TODO Get submission ids from client
# submit_all(TASKS["26"], "661")
# submit_all(TASKS["27"], "662")
