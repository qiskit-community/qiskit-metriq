import csv
import os
import statistics
from pyzx import routing
from qiskit import qiskit
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.transpiler import CouplingMap, TranspilerError
from qiskit_versions import get_release_date

SAMPLE_SIZE = 100
ARCHITECTURES = ['ibm_rochester', 'rigetti_16q_aspen']
OPTIMIZATION_LEVEL = 3
VERSION = qiskit.__version__
DATE = get_release_date(VERSION)
METHOD = f"Qiskit {VERSION} compilation"

def run_task(qasm_id: str):
  qasm_file_path = os.path.abspath(os.path.join( "..", "benchmarking",f"{qasm_id}.qasm"))
  circuit = QuantumCircuit.from_qasm_file(qasm_file_path)
  circuit_depth = []
  gate_count = []

  # Setup csv file
  # TODO setup files for individual runs
  output_path = os.path.abspath(os.path.join( "..","benchmarking","results",f"{qasm_id}-qiskit{VERSION}.csv"))
  output_file = open(output_path, "w")
  writer = csv.writer(output_file)
  header = ["name","method","date","platform","sample_size","seed","optimization_level","metric_name","metric_value"]
  writer.writerow(header)

  # Transpile for each architecture using pyzx
  for arch in ARCHITECTURES:
    architecture = routing.create_architecture(arch)
    coupling_map = CouplingMap(architecture.graph.edges())
    common_res = [f"{qasm_id}.qasm circuit benchmark",METHOD,DATE,architecture.name,SAMPLE_SIZE]

    for i in range(SAMPLE_SIZE):
        result = None
        while result is None:
            try:
                result = transpile(circuit, coupling_map=coupling_map, optimization_level=OPTIMIZATION_LEVEL,
                                   seed_transpiler=i)
            except TranspilerError:
                i += SAMPLE_SIZE
        depth = result.depth()
        gates = sum(result.count_ops().values())

        # Save locally
        circuit_depth.append(depth)
        gate_count.append(gates)

        # Save to file
        # TODO: Unique files and filenames for induvidual runs
        writer.writerow(common_res + [i,OPTIMIZATION_LEVEL,"circuit depth",depth])
        writer.writerow(common_res + [i,OPTIMIZATION_LEVEL,"gate count",gates])

    # Calc ave + stdev
    depth_ave = round(statistics.mean(circuit_depth))
    depth_stdev = round(statistics.stdev(circuit_depth),3)
    gate_count_ave = round(statistics.mean(gate_count))
    gate_count_stdev = round(statistics.stdev(gate_count),3)

    # Save ave and stdev results
    # TODO create separate file for metriq submission 
    writer.writerow(common_res + ["","","circuit depth",depth_ave])
    writer.writerow(common_res + ["","","circuit depth",depth_stdev])
    writer.writerow(common_res + ["","","gate count",gate_count_ave])
    writer.writerow(common_res + ["","","gate count",gate_count_stdev])

    # Reset result lists
    circuit_depth.clear()
    gate_count.clear()

  output_file.close()

run_task("ex1_226")