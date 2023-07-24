
import os
# import json
from metriq import MetriqClient
# from metriq.models.result import ResultCreateRequest

METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")

def hello_metriq():
  client = MetriqClient(token=METRIQ_TOKEN)
  print(client.hello())
  # >>> {'status': 'API is working', 'message': 'This is the Metriq public REST API.'}

# hello_metriq()

def process_results():
  folder_path = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "results"))
  filenames = os.listdir(folder_path)
  for filename in filenames:
    with open(os.path.join(folder_path, filename), "r") as file:
      content = file.read()
      print(content)
    print("-" * 25)

  # TODO:
  # 2. compute ave and std for each file (one for each architecture)
  # 3. create result item and add to client
  # 4. create metriq submission item
  # 5. submit item though metriq API

  client = MetriqClient(token=METRIQ_TOKEN)
  print(client.hello())

  # PLATFORM ENDPOINT
  # client.http.get(f"/platform/") #HttpClientError 200

  # TASK ENDPOINTS
  # response = client.http.get(f"/task/names/")
  # print(response["message"])
  # print(*response["data"], sep = "\n")
  # {'id': 26, 'name': 'ex1_226.qasm (Aspen)', 'top': 0}
  # {'id': 27, 'name': 'ex1_226.qasm (Rochester)', 'top': 0}

  # response = client.http.get(f"/task/26/")
  # print(response["message"])
  # print(json.dumps(response["data"], indent=4))

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

process_results()