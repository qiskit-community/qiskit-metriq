import pandas as pd
import os
import statistics
from pyzx import routing
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.transpiler import CouplingMap, TranspilerError
from qiskit_versions import get_version_date

try:
  # Try to import qiskit version from 0.44.0 and above
  from qiskit import __qiskit_version__
  VERSION = __qiskit_version__["qiskit"]
except ImportError:
  # Import from older versions
  import qiskit
  VERSION = qiskit.__version__

SAMPLE_SIZE = 100
ARCHITECTURES = ["ibm_rochester", "rigetti_16q_aspen"]
OPTIMIZATION_LEVEL = 3
DATE = get_version_date("qiskit", VERSION)
METHOD = f"Qiskit {VERSION} compilation"

def run_experiment(qasm_id: str):
  print(f"\nRunning {METHOD} for circuit {qasm_id}\n")

  qasm_file_path = os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking",f"{qasm_id}.qasm"))
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

    output_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..","benchmarking","results",f"{qasm_id}-qiskit{VERSION}-{arch}.csv"))
    df.to_csv(output_path, sep="|")

    print(f"{arch}\n",
          f"- Circuit depth - ave: {round(df['Circuit depth'].mean())} | stdev: {round(df['Circuit depth'].std(),3)}\n",
          f"- Gate count - ave: {round(df['Gate count'].mean())} | stdev: {round(df['Gate count'].std(),3)}")

run_experiment("ex1_226")