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

SAMPLE_SIZE = 100
ARCHITECTURES = ['ibm_rochester', 'rigetti_16q_aspen']

def average(lst):
    return sum(lst) / len(lst)

def run_task(output_file_name: str):
  circuit = QuantumCircuit.from_qasm_str(qasm_in)
  circuit_depth = []
  gate_count = []
  output_file = open(output_file_name, "w")
  print(f"Qiskit version: {qiskit.__version__}", file=output_file)
  print(f"Sample size: {SAMPLE_SIZE}\n", file=output_file)

  # transpile for each architecture using pyzx
  for arch in ARCHITECTURES:
      architecture = routing.create_architecture(arch)
      coupling_map = CouplingMap(architecture.graph.edges())
      print(f"Architecture: {architecture.name}", file=output_file)

      # TODO: use irange instead
      for i in range(SAMPLE_SIZE):
          # transpile
          result = transpile(circuit, coupling_map=coupling_map, optimization_level=3, seed_transpiler=i)
          circuit_depth.append(result.depth())
          gate_count.append(sum(result.count_ops().values()))

          # Uncomment the line below to see individual run outputs
          # print("Sample", i+1, "- Circuit depth:", result.depth(), "| Gate count:", sum(result.count_ops().values()))
      
      # Write to file

      output = "Circuit depth ave:" + str(average(circuit_depth)) + "| Gate count ave:" + str(average(gate_count)) + "\n"
      print(f"{output}", file=output_file)

      circuit_depth.clear()
      gate_count.clear()
  output_file.close()

# TODO Update the output file format to what is expected from metriq API
run_task("test_output.txt")


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

##############################################
# TODO: Fix error below on earlier qiskit-terra version:

$ python scripts/circuit_depth_and_gate_count.py
Qiskit version:  0.23.0
Sample size:  100
Architecture: ibm_rochester
Traceback (most recent call last):
  File "scripts/circuit_depth_and_gate_count.py", line 45, in <module>
    result = transpile(circuit, coupling_map=coupling_map, optimization_level=3)
  File "/Users/kspuldaro/opt/anaconda3/envs/metriq/lib/python3.7/site-packages/qiskit/compiler/transpiler.py", line 388, in transpile
    transpile_config["pass_manager_config"].backend_properties,
  File "/Users/kspuldaro/opt/anaconda3/envs/metriq/lib/python3.7/site-packages/qiskit/compiler/transpiler.py", line 474, in _serial_transpile_circuit
    result = pass_manager.run(circuit, callback=callback, output_name=output_name)
  File "/Users/kspuldaro/opt/anaconda3/envs/metriq/lib/python3.7/site-packages/qiskit/transpiler/passmanager.py", line 528, in run
    return super().run(circuits, output_name, callback)
  File "/Users/kspuldaro/opt/anaconda3/envs/metriq/lib/python3.7/site-packages/qiskit/transpiler/passmanager.py", line 228, in run
    return self._run_single_circuit(circuits, output_name, callback)
  File "/Users/kspuldaro/opt/anaconda3/envs/metriq/lib/python3.7/site-packages/qiskit/transpiler/passmanager.py", line 283, in _run_single_circuit
    result = running_passmanager.run(circuit, output_name=output_name, callback=callback)
  File "/Users/kspuldaro/opt/anaconda3/envs/metriq/lib/python3.7/site-packages/qiskit/transpiler/runningpassmanager.py", line 125, in run
    dag = self._do_pass(pass_, dag, passset.options)
  File "/Users/kspuldaro/opt/anaconda3/envs/metriq/lib/python3.7/site-packages/qiskit/transpiler/runningpassmanager.py", line 173, in _do_pass
    dag = self._run_this_pass(pass_, dag)
  File "/Users/kspuldaro/opt/anaconda3/envs/metriq/lib/python3.7/site-packages/qiskit/transpiler/runningpassmanager.py", line 202, in _run_this_pass
    new_dag = pass_.run(dag)
  File "/Users/kspuldaro/opt/anaconda3/envs/metriq/lib/python3.7/site-packages/qiskit/transpiler/passes/utils/gate_direction.py", line 299, in run
    return self._run_coupling_map(dag, layout_map)
  File "/Users/kspuldaro/opt/anaconda3/envs/metriq/lib/python3.7/site-packages/qiskit/transpiler/passes/utils/gate_direction.py", line 177, in _run_coupling_map
    f"Flipping of gate direction is only supported "
qiskit.transpiler.exceptions.TranspilerError: "Flipping of gate direction is only supported for ['cx', 'cz', 'ecr'] at this time, not 'swap'."
'''
