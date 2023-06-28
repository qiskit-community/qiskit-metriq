import pandas as pd
import os
import statistics
from pyzx import routing
from qiskit import qiskit
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.transpiler import CouplingMap, TranspilerError
from qiskit_versions import get_release_date

SAMPLE_SIZE = 100
ARCHITECTURES = ["ibm_rochester", "rigetti_16q_aspen"]
OPTIMIZATION_LEVEL = 3
VERSION = qiskit.__version__
DATE = get_release_date(VERSION)
METHOD = f"Qiskit {VERSION} compilation"

def run_task(qasm_id: str):
  qasm_file_path = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking",f"{qasm_id}.qasm"))
  circuit = QuantumCircuit.from_qasm_file(qasm_file_path)

  print(METHOD)
  print("Sample Size: ",SAMPLE_SIZE)

  # Transpile for each architecture using pyzx
  for arch in ARCHITECTURES:
    architecture = routing.create_architecture(arch)
    coupling_map = CouplingMap(architecture.graph.edges())
    df = pd.DataFrame(columns=["Qasm file","Method","Date","Opt level","Platform","Seed","Circuit depth","Gate count"])

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

    # Calc ave + stdev using pandas and send results for metriq submission
    # TODO: Move it to a post processing script that reads from generated csv files
    # metriq_results1 = {
    #   "Name":[f"{qasm_id}.qasm circuit benchmark"],
    #   "Method" :[METHOD],
    #   "Date":[DATE],
    #   "Sample Size":[SAMPLE_SIZE],
    #   "Platform":[arch],
    #   "Metric Name":["Circuit depth"],
    #   "Metric Value":[round(df["Circuit depth"].mean())],
    #   "Notes":[f"Seed:{i}, Version:{VERSION}, Opt Level:{OPTIMIZATION_LEVEL}, Stdev: {round(df['Circuit depth'].std(),3)}"]
    # }
    # metriq_results2 = {
    #   "Name":[f"{qasm_id}.qasm circuit benchmark"],
    #   "Method" :[METHOD],
    #   "Date":[DATE],
    #   "Sample Size":[SAMPLE_SIZE],
    #   "Platform":[arch],
    #   "Metric Name":["Gate count"],
    #   "Metric Value":[round(df["Gate count"].mean())],
    #   "Notes":[f"Seed:{i}, Version:{VERSION}, Opt Level:{OPTIMIZATION_LEVEL}, Stdev: {round(df['Gate count'].std(),3)}"]
    # }
    print(f"{arch}\n",
          f"- Circuit depth - ave: {round(df['Circuit depth'].mean())} | stdev: {round(df['Circuit depth'].std(),3)}\n",
          f"- Gate count - ave: {round(df['Gate count'].mean())} | stdev: {round(df['Gate count'].std(),3)}")

run_task("ex1_226")