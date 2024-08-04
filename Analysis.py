import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

startTime = datetime.now()
print(startTime)

# Path to data files. FIRST RUN DATA_TREATING.PY AND REARRANGE PATH
path = 'C:/Users/PC/Downloads/REYES/Data/pion_P4/Averaged/analysis/final'

# List all files and sort them
file_names = sorted([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])

# Map filenames to numerical identifiers
file_number_mapping = {i + 1: file_name for i, file_name in enumerate(file_names)}

#Reads the first column from a file and returns it as a list of floats.
def read_column(file_path):
    data = pd.read_csv(file_path, sep='\s+', header=None)
    return data[0].values

#Computes the bins using the jackknife technique.
def compute_bins(path, total_bins, num_rows=10):

    bins = [np.zeros(num_rows) for _ in range(total_bins)]

    for i in range(total_bins):
        bin_array = np.zeros(num_rows)
        count = 0
        for file_index in range(1, total_bins + 1):
            if file_index == i + 1:
                continue
            file_name = file_number_mapping.get(file_index, None)
            if file_name:
                file_path = os.path.join(path, file_name)
                column_data = read_column(file_path)
                bin_array += column_data[:num_rows]
                count += 1
        
        if count > 0:
            bin_array /= count
        bins[i] = bin_array

    return bins

# Parameters
total_bins = len(file_names)
bins = compute_bins(path, total_bins)

# Initialize E_eff with zeros
num_rows = 10
E_eff = np.mean(np.array(bins), axis=0)

# Computes E_efff and errors using jackknife resampling
E_efff = []
E_efff_errors = []

for i in range(num_rows - 1):
    log_ratios = [np.log(bin_array[i] / bin_array[i + 1]) for bin_array in bins if bin_array[i + 1] != 0]
    if not log_ratios:
        continue
    log_ratio_mean = np.mean(log_ratios)
    E_efff.append(log_ratio_mean)
    # Jackknife error
    error = np.sqrt((total_bins - 1) * np.mean((log_ratios - log_ratio_mean) ** 2))
    E_efff_errors.append(error)

# No NaN values in E_efff and E_efff_errors
E_efff = np.nan_to_num(E_efff, nan=0)
E_efff_errors = np.nan_to_num(E_efff_errors, nan=0)





# Range for the plateau
t_low = 5
t_high = 10

# Calculate the weighted sum 'a'
a = np.sum(E_efff[t_low-1:t_high] * (1 / E_efff_errors[t_low-1:t_high])**2)

plateau = a/ np.sum((1 / E_efff_errors[t_low-1:t_high])**2)

# Print the calculated weighted sum
print(f"Weighted sum a = {a}")

# Display the E_efff vector with errors
print("E_efff as vector is:", E_efff)
print("Errors:", E_efff_errors)

t_range = np.arange(t_low, t_high)

# Plot the E_efff vector with error bars
plt.figure(figsize=(10, 6))
plt.errorbar(np.arange(1, len(E_efff) + 1), E_efff, yerr=E_efff_errors, fmt='o', color='b', ecolor='g', capsize=5, label='E_efff')
plt.plot(t_range, [plateau] * len(t_range), 'r-', label=f'Plateu fit = {plateau:.5f}')
plt.title('Effective Energy at P = $\sqrt{32}$')
plt.xlabel('Time (t)')
plt.ylabel('$E_{eff}$')
plt.grid(True)
plt.legend()
plt.show()

print("Execution Time:", datetime.now() - startTime)
