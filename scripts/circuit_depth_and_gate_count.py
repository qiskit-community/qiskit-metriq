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
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.transpiler import CouplingMap

circuit = QuantumCircuit.from_qasm_str(qasm_in)

# transpile for each architecture using pyzx
for arch in ['ibm_rochester', 'rigetti_16q_aspen']:
    architecture = routing.create_architecture(arch)
    coupling_map = CouplingMap(architecture.graph.edges())

    # transpile
    result = transpile(circuit, coupling_map=coupling_map, optimization_level=3)
    print(architecture.name, result.depth(), sum(result.count_ops().values()))