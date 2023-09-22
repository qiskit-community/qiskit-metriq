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
method_col = "Method"
circuit_depth_col = "Circuit depth"
gate_count_col = "Gate count"

# Sort dataframes by date
aspen_combined_df.sort_values(by=date_col, inplace=True)
rochester_combined_df.sort_values(by=date_col, inplace=True)

# Extract version from Method column
version_col = "Qiskit version"
aspen_combined_df[version_col] = aspen_combined_df.apply(lambda row : str(row[method_col]).split(' ')[1], axis = 1)
rochester_combined_df[version_col] = rochester_combined_df.apply(lambda row : str(row[method_col]).split(' ')[1], axis = 1)

# Enable grid lines
sns.set(style="whitegrid")

# Create boxplots for aspen architecture
# Circuit depth
plt.figure(figsize=(10,6))
sns.boxplot(data=aspen_combined_df,x=version_col,y=circuit_depth_col)
plt.title(f"{circuit_depth_col} distribution of Qiskit compilation for {architectures['aspen']}")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
# Gate count
plt.figure(figsize=(10,6))
sns.boxplot(data=aspen_combined_df,x=version_col,y=gate_count_col)
plt.title(f"{gate_count_col} distribution of Qiskit compilation for {architectures['aspen']}")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Create boxplots for rochester architecture
# Circuit depth
plt.figure(figsize=(10,6))
sns.boxplot(data=rochester_combined_df,x=version_col,y=circuit_depth_col)
plt.title(f"{circuit_depth_col} distribution of Qiskit compilation for {architectures['rochester']}")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
# Gate count
plt.figure(figsize=(10,6))
sns.boxplot(data=rochester_combined_df,x=version_col,y=gate_count_col)
plt.title(f"{gate_count_col} distribution of Qiskit compilation for {architectures['rochester']}")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()



