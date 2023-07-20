
import os
from metriq import MetriqClient
from metriq.models.result import ResultCreateRequest

METRIQ_TOKEN = os.getenv("METRIQ_TOKEN")

def hello_metriq():
  client = MetriqClient(token=METRIQ_TOKEN)
  print(client.hello())
  # >>> {'status': 'API is working', 'message': 'This is the Metriq public REST API.'}

hello_metriq()