import os
from qiskit_versions import *

versions_info = get_qiskit_versions_info()

# Create a tox env for each qiskit version
for info in versions_info:
    # Since Python 3.6 and below have reached end of life
    # Using 3.7 here as it is compatible with all qiskit-terra versions
    python_version = "3.7"
    qiskit_version = info["version"]
    env_name = "q_v" + qiskit_version
    run_task_command = f"python {{toxinidir}}/scripts/circuit_depth_and_gate_count.py"
    tox_config = f"""[tox]
minversion = 3.7
envlist = {env_name}
[testenv]
usedevelop = True
deps =
    qiskit-terra=={qiskit_version}
    requests
    pyzx
commands = 
    {run_task_command}
"""
    absolute_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
    filename = absolute_path + '/tox.ini'
    run_tox_command = "tox -vre " + env_name

    print("... Creating tox config file...")

    with open(filename, 'w') as f:
        f.write(tox_config)
    
    os.system(run_tox_command)

"""
    Ideally, instead of overriding tox.ini content, only override qiskit version using tox CLI.
    For some reason it always installs the latest, defined in tox.ini

    # command = "tox -e "+ env_name + " -- pip install --qiskit-terra==" + qiskit_version
    # CLI commands tried directly on terminal:
    # tox -e q_0.20.0 -- pip install qiskit-terra==0.20.0
    # tox -e q_0.20.0 --force-dep qiskit-terra==0.20.0
    # tox -e q_0.20.0 -r --force-dep qiskit==0.20.0
"""