import os
from qiskit_versions import *

versions_info = get_qiskit_versions_info()

# Create a tox env for each qiskit version
for info in versions_info:
    version = info["version"]
    env_name = "qiskit v" + version

    # TODO: This does not override latest version defined in tox.ini. Keep looking into this.
    command = "tox -e "+ env_name + " -- pip install --qiskit-terra==" + version
    # CLI commands tried:
    # tox -e q_0.20.0 -- pip install qiskit-terra==0.20.0
    # tox -e q_0.20.0 --force-dep qiskit-terra==0.20.0
    # tox -e q_0.20.0 -r --force-dep qiskit==0.20.0

    # TODO: Uncomment line below when command actually works
    # os.system(command).
