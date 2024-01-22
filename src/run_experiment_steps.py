import os
from preprocessing import get_submissions_update_info, delete_submission_results
from env_setup import create_tox_config_file
# from pprint import pp

METRIQ_CLIENT_URL = "https://github.com/unitaryfund/metriq-client/tarball/development"

def get_results_path(experiment_name: str) -> str:
  return os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..","benchmarking",experiment_name,"results"))

def get_csv_files(qiskit_version: str, experiment_name: str) -> [str]:
    results_path = get_results_path(experiment_name)
    matching_files = []
    for filename in os.listdir(results_path):
        if "csv" in filename and qiskit_version in filename:
            matching_files.append(filename)
    return matching_files

# TODO: allow passing experiment_name to this script
experiment_name="ex1_226"

# Get summary of metriq submissions that need update (add/replace) based on new Qiskit versions
submissions_to_be_updated = get_submissions_update_info("qiskit") # Use "qiskit-terra" to run on Qiskit < v0.45.0
for key,value in submissions_to_be_updated.items():
    submission_id = key
    add_versions = value["add"]
    replace_versions = value["replace"]

    for replace_version in replace_versions:
        print(f"Replacing qiskit version {replace_version} results...")
        
        # Delete local csv results linked to replace_version
        results_path = get_results_path(experiment_name)
        files_to_be_deleted = get_csv_files(replace_version)
        for filename in files_to_be_deleted:
            print(f"Deleting CSV files for outdated qiskit version {replace_version}...")
            os.remove(os.path.join(results_path,filename))
        
        # Delete result items linked to replace_version from metriq submission
        print(f"Deleting qiskit version {replace_version} results from submission {submission_id}...")
        delete_submission_results(submission_id, replace_version)

    for new_qiskit_version in add_versions:
        print(f"Starting environment setup for qiskit version {new_qiskit_version}...")
        
        #Set up tox env config
        python_version = "3.11"
        env_name = "qiskit_v" + new_qiskit_version
        results_available = get_csv_files(new_qiskit_version)
        run_experiment_command = "python {{toxinidir}}/src/circuit_depth_and_gate_count.py" if not results_available else ""
        install_metriq_client_command = f"pip install --upgrade {METRIQ_CLIENT_URL}"
        submit_data_command = f"python {{toxinidir}}/src/postprocessing.py"
        env_var = submission_id
        commands = [run_experiment_command, install_metriq_client_command, submit_data_command]
        create_tox_config_file(python_version, env_name, new_qiskit_version, env_var, commands)
        
        # Run tox with new config
        print(f"Running experiment for qiskit version {new_qiskit_version}...")
        run_tox_command = "tox -vre " + env_name
        os.system(run_tox_command)
