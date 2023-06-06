#TODO: Move qasm code to its own file and load it here

qasm_in = """
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

SAMPLE_SIZE = 100
ARCHITECTURES = ['ibm_rochester', 'rigetti_16q_aspen']

def run_task(output_file_name: str):
  circuit = QuantumCircuit.from_qasm_str(qasm_in)
  circuit_depth = []
  gate_count = []

  # Setup csv file
  path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "results", output_file_name))
  output_file = open(path, "w")
  writer = csv.writer(output_file)
  header = ["name","method_name","qiskit_version","sample_size","platform_name","metric_name","metric_t1","metric_t1_value","metric_t2","metric_t2_value"]
  writer.writerow(header)

  # transpile for each architecture using pyzx
  for arch in ARCHITECTURES:
    architecture = routing.create_architecture(arch)
    coupling_map = CouplingMap(architecture.graph.edges())
    results = ["tket-ex1_226.qasm circuit benchmark","qiskit compilation",qiskit.__version__,SAMPLE_SIZE,architecture.name]

    for i in range(SAMPLE_SIZE):
        # transpile
        result = None
        while result is None:
            try:
                result = transpile(circuit, coupling_map=coupling_map, optimization_level=3,
                                   seed_transpiler=i)
                # print('seed_transpiler: ', i)
            except TranspilerError:
                # TODO: save seed value 
                i += SAMPLE_SIZE
        circuit_depth.append(result.depth())
        gate_count.append(sum(result.count_ops().values()))
    
    # Write to file
    r1 = results.copy()
    r1.extend(["circuit depth","ave",statistics.mean(circuit_depth),"stdev",round(statistics.stdev(circuit_depth),3)])
    writer.writerow(r1)

    r2 = results.copy()
    r2.extend(["gate count","ave",statistics.mean(gate_count),"stdev",round(statistics.stdev(gate_count),3)])
    writer.writerow(r2)

    circuit_depth.clear()
    gate_count.clear()
  output_file.close()

run_task(f"ex1_226-q{qiskit.__version__}.csv")
