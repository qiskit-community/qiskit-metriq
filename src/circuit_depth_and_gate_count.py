import os
import pandas as pd
from pyzx import routing
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap, TranspilerError
from qiskit_versions import *

VERSION = get_installed_version()
PACKAGE_NAME = "qiskit" if VERSION == compare_versions(VERSION, "0.25.3") else "qiskit-terra"
SAMPLE_SIZE = 100
ARCHITECTURES = ["ibm_rochester", "rigetti_16q_aspen"]
OPTIMIZATION_LEVEL = 3
DATE = get_version_date(PACKAGE_NAME, VERSION)
METHOD = f"{PACKAGE_NAME} {VERSION} compilation"

def run_experiment(qasm_id: str):
  print(f"\nRunning {METHOD} for circuit {qasm_id}\n")

  qasm_file_path = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..","benchmarking",qasm_id,f"{qasm_id}.qasm"))
  circuit = QuantumCircuit.from_qasm_file(qasm_file_path)
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

    output_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","benchmarking",qasm_id,"results",f"{qasm_id}-qiskit{VERSION}-{arch}.csv"))
    df.to_csv(output_path, sep="|")

    print(f"{arch}\n",
          f"- Circuit depth - ave: {df['Circuit depth'].mean()} | stdev: {df['Circuit depth'].std()}\n",
          f"- Gate count - ave: {df['Gate count'].mean()} | stdev: {df['Gate count'].std()}")

run_experiment("ex1_226")