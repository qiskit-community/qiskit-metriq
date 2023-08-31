import os
from fetch_qiskit_versions import get_qiskit_versions_info, write_versions_to_file

RESULTS_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..", "benchmarking", "results"))
METRIQ_CLIENT_URL = "https://github.com/unitaryfund/metriq-client/tarball/development"
EXPERIMENT = "circuit_depth_and_gate_count"
versions_info = get_qiskit_versions_info()

# Check if qiskit_version already has a result
def search_results(qiskit_version: str):
    for filename in os.listdir(RESULTS_PATH):
        if qiskit_version in filename:
            return True
    return False

# Check for matching major-minor version results to be replaced with latest
def replace_with_latest(qiskit_version: str) -> [str]:
    replace_files = []
    for filename in os.listdir(RESULTS_PATH):
        if "csv" in filename:
            filename_major_minor_patch = filename.split("-")[1].replace("qiskit","").split(".")
            input_major_minor_patch = qiskit_version.split(".")

            if (filename_major_minor_patch[0] == input_major_minor_patch[0]
                and filename_major_minor_patch[1] == input_major_minor_patch[1] 
                and filename_major_minor_patch[2] < input_major_minor_patch[2]):
                    replace_files.append(filename)
    return replace_files

# Create a tox env for each qiskit version
for info in versions_info:
    qiskit_version = info["version"]

    # Skip running the experiment if there are alredy results associated with that version
    if search_results(qiskit_version):
        continue
    
    replace_results = replace_with_latest(qiskit_version)
    if replace_results:
        for filename in replace_results:
            # Remove from folder
            os.remove(os.path.join(RESULTS_PATH,filename))
        # Update json file
        write_versions_to_file(versions_info)

    print("\nRun experiment for qiskit-terra version ", qiskit_version,"...\n")

    # TODO Pass python version and qasm file to tox env setup

    # Using 3.8 for now as it is compatible with all qiskit-terra versions
    python_version = "3.8"
    env_name = "q_v" + qiskit_version
    run_experiment_command = f"python {{toxinidir}}/src/{{EXPERIMENT}}.py"
    install_metriq_client_command = f"pip install --upgrade {{METRIQ_CLIENT_URL}}"
    submit_data_command = f"python {{toxinidir}}/src/postprocessing.py"
    numpy_version = "numpy<1.20"
    tox_config = f"""[tox]
minversion = {python_version}
envlist = {env_name}
[testenv]
usedevelop = True
deps =
    qiskit-terra=={qiskit_version}
    %s
    pandas
    pyzx
    requests
    tea-client==0.0.7
    tea-console==0.0.6
    typer==0.3.2
passenv = METRIQ_TOKEN
commands = 
    {run_experiment_command}
    ;{install_metriq_client_command}
    ;{submit_data_command}
""" %(numpy_version if qiskit_version in ["0.13.0", "0.14.2", "0.15.2"] else "")
    absolute_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), ".."))
    filename = absolute_path + "/tox.ini"
    run_tox_command = "tox -vre " + env_name

    #Create tox config file
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
    # tox -e q_0.20.0 --force-dep qiskit-terra==0.20.0
"""
