# Circuit benchmark task

Execute quantum circuit compilation [benchmark task 25](https://metriq.info/Task/25) and submit performance results for each version of Qiskit to metriq.info.

## Archictecture

Tox environments, with different Qiskit versions installed, execute [circuit benchmark tasks](https://github.com/qiskit-community/submit-metriq/blob/main/scripts/circuit_depth_and_gate_count.py), compiled for the `IBM-Q Rochester` and `Rigetti 16Q Aspen-1` architecture platforms.

## Requirements
* [tox](https://pypi.org/project/tox/)
* Python 3.8+


## Run locally
### To run benchmark task using the current stable version of `qiskit-terra`:
```bash
tox -e py38
```
**Note:**
To run a specific version of `qiskit-terra`, you can manually update it in the `tox.ini` file.
Versions >=0.13,<=0.15 require numpy<1.20. You can run the tox environments `terra13`, `terra14` or `terra15` as:
```bash
tox -e py8-terra13
```

### Create historical data using previous versions of  `qiskit-terra` since last update to Metriq:

```bash
python scripts/run_tox_envs.py
```
