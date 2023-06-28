import pandas as pd
import os
import statistics
from pyzx import routing
from qiskit import qiskit
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.transpiler import CouplingMap, TranspilerError
from qiskit_versions import get_release_date

SAMPLE_SIZE = 10
ARCHITECTURES = ["ibm_rochester", "rigetti_16q_aspen"]
OPTIMIZATION_LEVEL = 3
VERSION = qiskit.__version__
DATE = get_release_date(VERSION)
METHOD = f"Qiskit {VERSION} compilation"

def run_task(qasm_id: str):
  qasm_file_path = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking",f"{qasm_id}.qasm"))
  circuit = QuantumCircuit.from_qasm_file(qasm_file_path)

  # Transpile for each architecture using pyzx
  for arch in ARCHITECTURES:
    architecture = routing.create_architecture(arch)
    coupling_map = CouplingMap(architecture.graph.edges())
    df = pd.DataFrame(columns=["Qasm file","Method","Date","Opt Level","Platform","Seed","Circuit Depth","Gate count"])

    for i in range(SAMPLE_SIZE):
      result = None
      while result is None:
          try:
              result = transpile(circuit, coupling_map=coupling_map, optimization_level=OPTIMIZATION_LEVEL,
                                  seed_transpiler=i)
          except TranspilerError:
              i += SAMPLE_SIZE
      results = [f"{qasm_id}.qasm", METHOD, DATE, OPTIMIZATION_LEVEL,arch,i,result.depth(),sum(result.count_ops().values())]
      df.loc[len(df)] = results

    output_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","benchmarking","results",f"{qasm_id}-qiskit{VERSION}-{arch}.csv"))
    df.to_csv(output_path, sep="|")

  # TODO: Calc ave + stdev using pandas and store results in a separate file for metriq submission
  # metriq_results = {
  #   "Name":[f"{qasm_id}.qasm circuit benchmark"],
  #   "Method" :[METHOD],
  #   "Date":[DATE],
  #   "Sample Size":[SAMPLE_SIZE],
  #   "Platform":[],
  #   "Metric Name":[],
  #   "Metric Value":[],
  #   "Notes":["Seed:, Version:, Opt Level:"],
  # }

run_task("ex1_226")