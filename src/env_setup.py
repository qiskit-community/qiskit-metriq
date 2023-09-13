import os
from qiskit_versions import compare_versions

def create_tox_config_file(py_version:str, env_name:str, qiskit_version: str, commands: []): 
    # Use qiskit-terra for versions <= 0.25.0
    package_name = "qiskit" if qiskit_version == compare_versions(qiskit_version,"0.25.0") else "qiskit-terra"
    commands = "\n".join(commands)
    tox_config = f"""[tox]
        minversion = {py_version}
        envlist = {env_name}
        [testenv]
        usedevelop = True
        deps =
            {package_name}=={qiskit_version}
            %s
            pandas
            pyzx
            requests
            tea-client==0.0.7
            tea-console==0.0.6
            typer==0.3.2
        passenv = METRIQ_TOKEN
        commands = {commands}
        """
    absolute_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), ".."))
    filename = absolute_path + "/tox.ini"

    with open(filename, 'w') as f:
        f.write(tox_config)