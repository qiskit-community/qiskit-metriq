import os
from preprocessing import get_submissions_filtered_data, delete_outdated_result
from env_setup import create_tox_config_file

RESULTS_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ),"..", "benchmarking", "results"))
METRIQ_CLIENT_URL = "https://github.com/unitaryfund/metriq-client/tarball/development"
EXPERIMENT = "circuit_depth_and_gate_count"


def get_result_files(qiskit_version: str) -> [str]:
    matching_files = []
    for filename in os.listdir(RESULTS_PATH):
        if "csv" in filename and qiskit_version in filename:
            matching_files.append(filename)
    return matching_files

# Get filtered data from submissions 
submissions_filtered_data = get_submissions_filtered_data()

for key,value in submissions_filtered_data.items():
    submission_id = key
    add_versions = value["add"]
    replace_versions = value["replace"]

    # for a_version in add_versions:
        # Run experiment with new qiskit version
        # Post process results and submit to metriq
    
    for r_version in replace_versions:
        # Delete csv results linked to r_version
        files_to_be_deleted = get_result_files(r_version)
        for filename in files_to_be_deleted:
            os.remove(os.path.join(RESULTS_PATH,filename))
        
        # Delete result items linked to r_version from submission
        delete_outdated_result(submission_id, r_version)

# qiskit_versions_info = get_qiskit_versions_info()
# for info in qiskit_versions_info:
#     qiskit_version = info["version"]

#     # Skip running the experiment if there are alredy results associated with that version
#     if search_results(qiskit_version):
#         continue
    
#     replace_results = replace_with_latest(qiskit_version)
#     if replace_results:
#         for filename in replace_results:
#             # Remove from folder
#             os.remove(os.path.join(RESULTS_PATH,filename))
#         # Update json file
#         write_versions_to_file(qiskit_versions_info)

#     print("\nRun experiment for qiskit-terra version ", qiskit_version,"...\n")

#     # Create a tox env for each qiskit version
#     # TODO Pass python version and qasm file to tox env setup
#     python_version = "3.8"
#     env_name = "q_v" + qiskit_version
#     run_experiment_command = f"python {{toxinidir}}/src/{{EXPERIMENT}}.py"
#     install_metriq_client_command = f"pip install --upgrade {{METRIQ_CLIENT_URL}}"
#     submit_data_command = f"python {{toxinidir}}/src/postprocessing.py"
#     commands = [run_experiment_command, install_metriq_client_command, submit_data_command]
#     create_tox_config_file(python_version, env_name, qiskit_version, commands)
    
#     # Run tox with new config
#     run_tox_command = "tox -vre " + env_name
#     os.system(run_tox_command)

"""
    Ideally, instead of overriding tox.ini content, only override qiskit version using tox CLI.
    For some reason it always installs the latest, defined in tox.ini

    # command = "tox -e "+ env_name + " -- pip install --qiskit-terra==" + qiskit_version
    # CLI commands tried directly on terminal:
    # tox -e q_0.20.0 -- pip install qiskit-terra==0.20.0
    # tox -e q_0.20.0 --force-dep qiskit-terra==0.20.0
    # tox -e q_0.20.0 --force-dep qiskit-terra==0.20.0
"""
