# Circuit benchmark task

Execute [circuit benchmark task 25](https://metriq.info/Task/25) and submit performance results for each version of Qiskit to metriq.info.

## Archictecture

Tox enviroments that install different versions of Qiskit and execute [circuit benchmark task](https://github.com/qiskit-community/submit-metriq/blob/main/scripts/circuit_depth_and_gate_count.py), transpiled for the `IBMq Rochester` and `Rigetti 16Q Aspen-1` architecture platforms.

## Requirements
* [tox](https://pypi.org/project/tox/)
* Python 3.8+


## Run locally
### To run benchmark task using the current stable version of `qiskit-terra`:
```bash
tox
```
**Note:**
To run a specific version of `qiskit-terra`, you can manually update it in the `tox.ini` file.

### Create historical data using previous versions of  `qiskit-terra` since last update to Metriq:

```bash
python scripts/run_tox_envs.py
```

## Troubleshooting
Known `qiskit-terra` versions that fail executing the task:
* 0.13.0
* 0.14.2
* 0.15.2
