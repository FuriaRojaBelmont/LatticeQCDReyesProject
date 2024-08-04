import os
import numpy as np
import pandas as pd

#This code takes the positive and negative data from each folder in pion_P'x' and averages them into CSV files in a folder called 'Averaged'.
#Then, as a special case, it only takes the first 64 rows of the files in 'Averaged' and creates new CSVs with them, leaving only the moments 0 0 (+-)4. These are deposited in the folder 'analysis'.
#Finally, it takes the files from 'analysis' and averages them again, this time among themselves: it leaves the first data point intact, the second one is averaged with the penultimate, the third with the antepenultimate, and so on until the last data point, which is also left intact. It creates CSVs for these new averages and stores them in the folder 'final'.
#The final interest is the folder called 'final' which contains the C(t) coefficients needed to plot with the file 'Analysis.py'.


#IT IS NECESSARY TO ALTER THE PATHS MENTIONED HERE, AS THEY DEPEND ON WHERE THE FILES ARE LOCATED ON EACH COMPUTER.


# Initial file path template
file_path_template = 'C:/Users/PC/Downloads/REYES/Data/pion_P2/pion_P2/{}'

# Output directory
output_directory = 'C:/Users/PC/Downloads/REYES/Data/pion_P2/Averaged'
os.makedirs(output_directory, exist_ok=True)

# Range of directories to process
directories = range(0, 2400, 2)

# Initialize an empty list to hold the resulting arrays for each directory
results = []
last_data_length = None

for dir_number in directories:
    directory_path = file_path_template.format(dir_number)
    
    file_path1 = directory_path + '/twop_momforsmear_+0_+0_+2_zeta_-0.8000_dir_z.dat'
    file_path2 = directory_path + '/twop_momforsmear_+0_+0_-2_zeta_-0.8000_dir_z.dat'
    
    if not os.path.exists(file_path1) or not os.path.exists(file_path2):
        print(f"File not found in directory: {directory_path}")
        if last_data_length is not None:
            combined_data = np.zeros(last_data_length)
            output_file_path = os.path.join(output_directory, f'{dir_number}.csv')
            np.savetxt(output_file_path, combined_data, delimiter=',')
            print(f"Created zero-filled file for directory {directory_path} due to missing files.")
        continue

    # Read the 4th column of both files, this is the C(t) function of the files
    try:
        data1 = np.loadtxt(file_path1, usecols=4)
        data2 = np.loadtxt(file_path2, usecols=4)
        last_data_length = data1.shape[0]
    except Exception as e:
        print(f"Error reading files in directory {directory_path}: {e}")
        if last_data_length is not None:
            combined_data = np.zeros(last_data_length)
            output_file_path = os.path.join(output_directory, f'{dir_number}.csv')
            np.savetxt(output_file_path, combined_data, delimiter=',')
            print(f"Created zero-filled file for directory {directory_path} due to read error.")
        continue

    # Ensures that both files have the same length
    if data1.shape != data2.shape:
        print(f"Files in directory {directory_path} have different shapes.")
        continue

    # This averages the data
    combined_data = (data1 + data2) / 2

    # Appends the result to the list
    results.append(combined_data)

    # Saves the averaged data to a CSV file
    output_file_path = os.path.join(output_directory, f'{dir_number}.csv')
    np.savetxt(output_file_path, combined_data, delimiter=',')
    
    print(f"Processed and saved directory: {directory_path}")

print("Processing complete. Averaged files have been saved.")

#FOR CASE 0 0 (+-)4 ONLY!! FOR A GENERALISED VERSION TRY AVERAGEEQUALMOMENTA.PY!!!

input_dir = 'C:/Users/PC/Downloads/REYES/Data/pion_P2/Averaged'
output_dir = 'C:/Users/PC/Downloads/REYES/Data/pion_P2/Averaged/analysis'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop through all the files in the input directory
for file_name in os.listdir(input_dir):
    input_file_path = os.path.join(input_dir, file_name)
    
    # Check if the file is a CSV file
    if os.path.isfile(input_file_path) and input_file_path.endswith('.csv'):
        # Read the first 64 rows and first 4 columns of the CSV file
        df = pd.read_csv(input_file_path, nrows=64)
        
        # Define the output file path
        output_file_path = os.path.join(output_dir, file_name)
        
        # Save the first 64 rows and 4 columns to a new CSV file
        df.to_csv(output_file_path, index=False)
        
        print(f'Saved first 64 rows and 4 columns of {file_name} to {output_file_path}')

print('Process completed.')

def process_file(file_path):
    data = pd.read_csv(file_path, header=None).values.flatten()
    
    
    final = []
    n = len(data)
    
    # Process the first value
    final.append(data[0])
    
    # Process the averaged pairs
    for i in range(1, n // 2):
        averaged_value = (data[i] + data[n - i - 1]) / 2
        final.append(averaged_value)
    
    # Process the middle value for even number of elements
    if n % 2 == 0:
        final.append(data[n // 2 - 1])
    
    return final

# List of file paths
file_paths = []  # Add your file paths here

for index in range(0, 2400, 2):
    file_paths.append('C:/Users/PC/Downloads/REYES/Data/pion_P2/Averaged/analysis/' + f'{index}.csv')
    

# Process each file and store results in separate lists
final_lists = []
output_dir1= 'C:/Users/PC/Downloads/REYES/Data/pion_P2/Averaged/analysis/final'
os.makedirs(output_dir1, exist_ok=True)

for idx, file_path in enumerate(file_paths):
    final_list = process_file(file_path)
    final_lists.append(final_list)
    print(f"Final list {idx}: {final_list}")

# Saves the final lists to new CSV files
for idx, final_list in enumerate(final_lists):
    output_path = 'C:/Users/PC/Downloads/REYES/Data/pion_P2/Averaged/analysis/final/'+ f"{idx}.csv"
    pd.DataFrame(final_list).to_csv(output_path, index=False, header=False)
