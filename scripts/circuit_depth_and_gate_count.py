#TODO: Move qasm code to its own file and load it here

ex1_226_qasm_in = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
creg c[16];
cx q[3],q[0];
cx q[1],q[0];
cx q[5],q[0];
x q[2];
cx q[2],q[0];
x q[4];
cx q[4],q[0];
"""

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

def run_task(output_file_name: str):
  circuit = QuantumCircuit.from_qasm_str(ex1_226_qasm_in)
  circuit_depth = []
  gate_count = []

  # Setup csv file
  path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "results", output_file_name))
  output_file = open(path, "w")
  writer = csv.writer(output_file)
  date = get_release_date(VERSION)
  header = ["name","method","qiskit_version","date","platform","sample_size","seed","optimization_level","metric_name","metric_value"]
  writer.writerow(header)

  # Transpile for each architecture using pyzx
  for arch in ARCHITECTURES:
    architecture = routing.create_architecture(arch)
    coupling_map = CouplingMap(architecture.graph.edges())
    results = ["ex1_226.qasm circuit benchmark","qiskit compilation",VERSION,date,architecture.name]

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
        writer.writerow(results + [SAMPLE_SIZE,i,OPTIMIZATION_LEVEL,"circuit depth",depth])
        writer.writerow(results + [SAMPLE_SIZE,i,OPTIMIZATION_LEVEL,"gate count",gates])

    # Calc ave + stdev
    depth_ave = round(statistics.mean(circuit_depth))
    depth_stdev = round(statistics.stdev(circuit_depth),3)
    gate_count_ave = round(statistics.mean(gate_count))
    gate_count_stdev = round(statistics.stdev(gate_count),3)

    # Save to file
    writer.writerow(results + [SAMPLE_SIZE,"","","circuit depth - ave",depth_ave])
    writer.writerow(results + [SAMPLE_SIZE,"","","circuit depth - stdev",depth_stdev])
    writer.writerow(results + [SAMPLE_SIZE,"","","gate count - ave",gate_count_ave])
    writer.writerow(results + [SAMPLE_SIZE,"","","gate count - stdev",gate_count_stdev])

    # Reset result lists
    circuit_depth.clear()
    gate_count.clear()

  output_file.close()

run_task(f"ex1_226-qiskit{VERSION}.csv")
