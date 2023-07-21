
import os
from metriq import MetriqClient
from metriq.models.result import ResultCreateRequest

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

  # client = MetriqClient(token=METRIQ_TOKEN)
  # methods = client.method_names_get()
  # print(*methods, sep = "\n")

  # print(client.task_names_get()) #400: Request validation error
  # print(client.task_get("26")) #ex1_226.qasm (Aspen) #400: Request validation error
  # print(client.task_get("27")) #ex1_226.qasm (Rochester) #400: Request validation error

  # Result attributes from https://github.com/unitaryfund/metriq-client/blob/development/metriq/models/result.py
  # Create result item

  # result = ResultCreateRequest()
  # result.task = "26" #ex1_226.qasm (Aspen)
  # result.method = "Qiskit compilation"
  # result.metricName = "gate count"
  # result.metricValue = ""
  # result.evaluatedAt = ""
  # result.isHigherBetter = "false"
  # result.sampleSize = SAMPLE_SIZE
  # result.notes = f"qiskit-terra version: {VERSION}, optimization level {OPTIMIZATION_LEVEL}, gate count stdev: {gate_count_stdev}"

  # client.result_add(result)
  # result = client.result_metric_names()
  # print(result)

process_results()