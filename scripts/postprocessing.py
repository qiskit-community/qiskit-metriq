
import os
import pandas as pd
from metriq import MetriqClient
# from metriq.models.result import ResultCreateRequest

METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")
RESULTS_PATH = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "results"))

def submit_all():
  filenames = os.listdir(RESULTS_PATH)
  for filename in filenames:
    file_path = os.path.join(RESULTS_PATH, f"{filename}")
    df = pd.read_csv(file_path, sep='|')
    process_results(df)

def process_results(dataframe):
  # columns = dataframe.columns.tolist()
  # print(columns)
  # Compute ave and std for each file (one for each architecture)
  circuit_depth_mean = dataframe["Circuit depth"].mean() #KeyError: 'Circuit depth'
  print("Circuit depth mean: ", circuit_depth_mean)

  # TODO:
  # 3. create result item 
  # 4. add result item client
  # 4. create metriq submission item
  # 5. submit item though metriq API

  # client = MetriqClient(token=METRIQ_TOKEN)
  # print(client.hello())

  # PLATFORM ENDPOINT
  # client.http.get(f"/platform/") #HttpClientError 200

  # TASK ENDPOINTS
  # response = client.http.get(f"/task/names/")
  # print(response["message"])
  # print(*response["data"], sep = "\n")
  # {'id': 26, 'name': 'ex1_226.qasm (Aspen)', 'top': 0}
  # {'id': 27, 'name': 'ex1_226.qasm (Rochester)', 'top': 0}

  # TODO: Create result item
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

submit_all()