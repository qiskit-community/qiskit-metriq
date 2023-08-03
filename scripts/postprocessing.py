
import os
import pandas as pd
from metriq import MetriqClient
from metriq.models.result import ResultCreateRequest

METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")
RESULTS_PATH = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "results"))
TASKS = {"25": "ex1_226.qasm", "26": "ex1_226.qasm (Aspen)", "27": "ex1_226.qasm (Rochester)"}

def submit_all(task):
  filenames = os.listdir(RESULTS_PATH)

  for filename in filenames:
    architectures = ["aspen", "rochester"]
    for arch in architectures:
      if arch in filename and arch in task.lower():
        file_path = os.path.join(RESULTS_PATH, f"{filename}")
        df = pd.read_csv(file_path, sep='|')
        process_results(df, task)

def process_results(dataframe, task):
  client = MetriqClient(token=METRIQ_TOKEN)
  # print(client.hello())

  metrics = ["Circuit depth", "Gate count"]
  for metric in metrics:
    result = ResultCreateRequest()
    result.task = task
    result.platform = dataframe["Platform"].iloc[0]
    result.method = "Qiskit compilation"
    result.metricName = metric
    result.metricValue = dataframe[metric].mean()
    result.evaluatedAt = dataframe["Date"].iloc[0]
    result.isHigherBetter = False
    # result.sampleSize = len(dataframe.index) object has no field "sampleSize"

    # Get extra info and add to notes
    sample_size = len(dataframe.index)
    metric_std = dataframe[metric].std()
    opt_level = dataframe["Opt level"].iloc[0]
    version = dataframe["Method"].iloc[0].split(" ")[1]
    result.notes = f"Stdev: {round(metric_std,3)}, Optimization level:{opt_level}, qiskit-terra version:{version}, sample size: {sample_size}"

  # TODO:
  # - add result item client
  # - create metriq submission item
  # - submit item though metriq API

  # client.result_add(result) #missing 1 required positional argument: 'submission_id'
  # print(client.result_metric_names())

submit_all(TASKS["26"])