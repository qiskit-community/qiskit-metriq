import os
from preprocessing import get_submissions_filtered_data, delete_submission_results
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

    for r_version in replace_versions:
        # Delete csv results linked to r_version
        files_to_be_deleted = get_result_files(r_version)
        for filename in files_to_be_deleted:
            os.remove(os.path.join(RESULTS_PATH,filename))
        # Delete result items linked to r_version from submission
        delete_submission_results(submission_id, r_version)

    for new_qiskit_version in add_versions:
        # Run experiment and submit results to metriq
        # Set up tox env config
        print(f"Starting setup for experiment run on qiskit version {new_qiskit_version}...")
        python_version = "3.8"
        env_name = "qiskit_v" + new_qiskit_version
        run_experiment_command = f"python {{toxinidir}}/src/{EXPERIMENT}.py"
        install_metriq_client_command = f"pip install --upgrade {METRIQ_CLIENT_URL}"
        submit_data_command = f"python {{toxinidir}}/src/postprocessing.py"
        env_var = submission_id
        commands = [run_experiment_command, install_metriq_client_command, submit_data_command]
        create_tox_config_file(python_version, env_name, new_qiskit_version, env_var, commands)
        
        # Run tox with new config
        print(f"Running experiment for qiskit version {new_qiskit_version}...")
        run_tox_command = "tox -vre " + env_name
        os.system(run_tox_command)
