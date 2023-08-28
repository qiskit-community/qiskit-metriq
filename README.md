# Qiskit compilation benchmark for Quantum circuits

Execute quantum circuit compilation [benchmark task 25](https://metriq.info/Task/25) and submit performance results for each version of Qiskit to [metriq.info](https://metriq.info/), a community-driven platform for hosting quantum benchmarks.

## Archictecture

This project creates a tox environment for each qiskit-terra version, starting from v0.13.0 to [latest](https://github.com/Qiskit/qiskit/releases).

The benchmark circuit compilation is batch processed, and the results are submitted to [metriq.info](https://metriq.info/).

Benchmark tasks for quantum computer compilers:
- ex1_226.qasm benchmark circuit
    - [Task 25](https://metriq.info/Task/25)
    - [Task 26](https://metriq.info/Task/26) - Aspen architecture
    - [Task 27](https://metriq.info/Task/27) - IBMQ Rochester architecture

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
