
import os
import pandas as pd
from metriq import MetriqClient
# from metriq.models.result import ResultCreateRequest

METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")
RESULTS_PATH = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "results"))
TASKS = {"25": "ex1_226.qasm", "26": "ex1_226.qasm (Aspen)", "27": "ex1_226.qasm (Rochester)"}

def submit_all(task):
  filenames = os.listdir(RESULTS_PATH)

  for filename in filenames:
    architectures = ["aspen", "rochester"]
    for arch in architectures:
      if arch in filename and arch in task.lower():
        print(arch)
        file_path = os.path.join(RESULTS_PATH, f"{filename}")
        df = pd.read_csv(file_path, sep='|')
        process_results(df, task)

def process_results(dataframe, task):
  metrics = ["Circuit depth", "Gate count"]
  for metric in metrics:
    print(metric,"ave: ", dataframe[metric].mean())
    print(metric,"std: ", dataframe[metric].std())
  print("---")

  # TODO:
  # - Gather relevant results from csv
  # - create result item 
  # - add result item client
  # - create metriq submission item
  # - submit item though metriq API

  client = MetriqClient(token=METRIQ_TOKEN)
  print(client.hello())
  
  # result = ResultCreateRequest()
  # result.task = "ex1_226.qasm (Aspen)"
  # result.platform = "Rigetti 16Q Aspen-1"
  # result.method = "Qiskit compilation"
  # result.metricName = "Circuit depth"
  # result.metricValue = 
  # result.evaluatedAt = "Rigetti 16Q Aspen-1"
  # result.isHigherBetter = false
  # result.sampleSize = SAMPLE_SIZE
  # result.notes = ""

  # client.result_add(result)
  # print(client.result_metric_names())

submit_all(TASKS["26"])