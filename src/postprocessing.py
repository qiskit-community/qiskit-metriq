
import os
import pandas as pd
from metriq import MetriqClient
from metriq.models.result import ResultCreateRequest
from metriq.models.submission import (Submission, SubmissionCreateRequest)

CONTENT_URL = "https://github.com/qiskit-community/submit-metriq"
THUMBNAIL_URL = "https://avatars.githubusercontent.com/u/30696987?s=200&v=4"
METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")
RESULTS_PATH = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "results"))
TASKS = {"25": "ex1_226.qasm", "26": "ex1_226.qasm (Aspen)", "27": "ex1_226.qasm (Rochester)"}
METHOD = "Qiskit compilation"
TAGS = ["quantum circuits", "compiler", "compilation", "ibm qiskit"]

def get_method_id(client: MetriqClient, method_name: str) -> str:
  # all_methods = client.method_get_names() # ERROR: AttributeError: 'MetriqClient' object has no attribute 'method_get_names'
  all_methods = client.http.get("/method/names/")["data"]
  for method in all_methods:
      if method["name"] == method_name:
        return method["id"]

def submit_all(task_name: str, submission_id: str):
  client = MetriqClient(token=METRIQ_TOKEN)
  # submission = create_submission(client,task_name) # TODO Uncomment this line when historical data for taska 26-27 are finalized
  # submission = client.submisson_get(submission_id)
  method_id = get_method_id(client, METHOD)
  task_id = list(TASKS.keys())[list(TASKS.values()).index(task_name)]
  client.submission_add_task(submission_id, task_id)
  client.submission_add_method(submission_id, method_id)

  for tag in TAGS:
    client.submission_add_tag(submission_id, tag)

  # TODO Need to find a way to to update params below (open issues in metriq-client)
  # submission.codeUrl
  # submission.platform
  
  # Process results and add them to submission
  # filenames = os.listdir(RESULTS_PATH)
  # for filename in filenames:
  #   architectures = ["aspen", "rochester"]
  #   for arch in architectures:
  #     if arch in filename and arch in task_name.lower():
  #       file_path = os.path.join(RESULTS_PATH, f"{filename}")
  #       df = pd.read_csv(file_path, sep='|')
  #       process_results(df, task_name, client, submission_id)

def create_submission(client: MetriqClient, task_name: str) -> Submission:
  submission_req = SubmissionCreateRequest()
  submission_req.name = task_name
  submission_req.contentUrl = CONTENT_URL
  submission_req.thumbnailUrl = THUMBNAIL_URL
  submission_req.description = f"Qiskit compilation for {task_name} benchmark circuit"
  return client.submission_add(submission_req)

def process_results(dataframe, task_name: str, client: MetriqClient, submission_id: str):
  metrics = ["Circuit depth", "Gate count"]
  for metric in metrics:
    result_item = ResultCreateRequest()
    result_item.task = task_name
    result_item.platform = dataframe["Platform"].iloc[0]
    result_item.method = METHOD
    result_item.metricName = metric
    result_item.metricValue = round(dataframe[metric].mean())
    result_item.evaluatedAt = dataframe["Date"].iloc[0]
    result_item.isHigherBetter = "false"
    # result_item.sampleSize = len(dataframe.index) # ERROR: object has no field "sampleSize"

    # Get extra info and add to notes
    sample_size = len(dataframe.index)
    metric_std = dataframe[metric].std()
    opt_level = dataframe["Opt level"].iloc[0]
    version = dataframe["Method"].iloc[0].split(" ")[1]
    result_item.notes = f"Stdev: {round(metric_std,3)}, Optimization level:{opt_level}, qiskit-terra version:{version}, sample size: {sample_size}"
    print("result_item:")
    print(result_item)

    client.result_add(result_item, submission_id) # ERROR: tea_client.errors.HttpClientError: HttpClientError(500: You broke it!!!)

submit_all(TASKS["26"], "661") # submission #661
submit_all(TASKS["27"], "662") # submission #662