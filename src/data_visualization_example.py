import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob

# All results
csv_files = glob.glob(os.path.abspath(os.path.join( os.path.dirname( __file__ ),"..", "benchmarking", "results", "*.csv")))

# Filter by architecture
architectures = {"aspen" : "rigetti_16q_aspen", "rochester" : "ibm_rochester"}
aspen_files = [file for file in csv_files if architectures["aspen"] in file]
rochester_files = [file for file in csv_files if architectures["rochester"] in file]

# Store dataframes by architecture
aspen_dataframes = []
rochester_dataframes = []

# For each architecture, read each file and store its dataframe
for csv_file_path in aspen_files:
  df = pd.read_csv(csv_file_path, sep="|")
  aspen_dataframes.append(df)

for csv_file_path in rochester_files:
  df = pd.read_csv(csv_file_path, sep="|")
  rochester_dataframes.append(df)

# Concatenate all dataframes by architecture
aspen_combined_df = pd.concat(aspen_dataframes, ignore_index=True)
rochester_combined_df = pd.concat(rochester_dataframes, ignore_index=True)

# Get data columns for plotting chart
date_col = "Date"
method_col = "Method" # Includes qiskit version info
circuit_depth_col = "Circuit depth"
gate_count_col = "Gate count"

# Sort dataframes by date
aspen_combined_df.sort_values(by=date_col, inplace=True)
rochester_combined_df.sort_values(by=date_col, inplace=True)

# Extract version from Method column
version_col = "Qiskit version"
aspen_combined_df[version_col] = aspen_combined_df.apply(lambda row : str(row[method_col]).split(' ')[1], axis = 1)
rochester_combined_df[version_col] = rochester_combined_df.apply(lambda row : str(row[method_col]).split(' ')[1], axis = 1)

# Create boxplots for aspen architecture
def create_boxplot(column: str, arch: str):
  sns.set(style="whitegrid")
  plt.figure(figsize=(10,6))
  combined_df = aspen_combined_df if "aspen" in arch else rochester_combined_df
  sns.boxplot(data=combined_df,x=version_col,y=column,palette="pastel")
  plt.title(f"{column} distribution of Qiskit compilation for {architectures[arch]} architecture")
  plt.xticks(rotation=90)
  plt.tight_layout()
  plt.show()

for arch in architectures:
  create_boxplot(circuit_depth_col, arch)
  create_boxplot(gate_count_col, arch)



