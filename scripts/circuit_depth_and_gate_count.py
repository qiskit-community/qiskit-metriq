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

from pyzx import routing
from qiskit import qiskit
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.transpiler import CouplingMap

print("Qiskit version: ", qiskit.__version__, "\n")

SAMPLE_SIZE = 100

def average(lst):
    return sum(lst) / len(lst)

circuit = QuantumCircuit.from_qasm_str(qasm_in)
circuit_depth = []
gate_count = []

# transpile for each architecture using pyzx
for arch in ['ibm_rochester', 'rigetti_16q_aspen']:
    architecture = routing.create_architecture(arch)
    coupling_map = CouplingMap(architecture.graph.edges())
    print("Architecture:", architecture.name)

    for i in range(SAMPLE_SIZE):
        # transpile
        result = transpile(circuit, coupling_map=coupling_map, optimization_level=3)
        circuit_depth.append(result.depth())
        gate_count.append(sum(result.count_ops().values()))
        
        # Uncomment the line below to see individual run outputs
        # print("Sample", i+1, "- Circuit depth:", result.depth(), "| Gate count:", sum(result.count_ops().values()))
    
    if len(circuit_depth) == SAMPLE_SIZE:
        print("Circuit depth ave:", average(circuit_depth), "| Gate count ave:", average(gate_count), "\n")
        circuit_depth.clear()
        gate_count.clear()

'''
Using SAMPLE_SIZE = 5

$ python scripts/circuit_depth_and_gate_count.py
Qiskit version:  0.23.3

Architecture: ibm_rochester
Sample 1 - Circuit depth: 9 | Gate count: 13
Sample 2 - Circuit depth: 9 | Gate count: 13
Sample 3 - Circuit depth: 10 | Gate count: 16
Sample 4 - Circuit depth: 10 | Gate count: 17
Sample 5 - Circuit depth: 12 | Gate count: 23
Circuit depth ave: 10.0 | Gate count ave: 16.4

Architecture: rigetti_16q_aspen
Sample 1 - Circuit depth: 8 | Gate count: 12
Sample 2 - Circuit depth: 8 | Gate count: 12
Sample 3 - Circuit depth: 6 | Gate count: 9
Sample 4 - Circuit depth: 8 | Gate count: 12
Sample 5 - Circuit depth: 8 | Gate count: 14
Circuit depth ave: 7.6 | Gate count ave: 11.8
'''
