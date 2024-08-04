import os
import numpy as np
import pandas as pd
from datetime import datetime
startTime = datetime.now()

#This code takes the positive and negative data from each folder in pion_P'x' and averages them into CSV files in a folder called 'Averaged'.
#Then, as a special case, it only takes the first 64 rows of the files in 'Averaged' and creates new CSVs with them, leaving only the moments 0 0 (+-)4. These are deposited in the folder 'analysis'.
#Finally, it takes the files from 'analysis' and averages them again, this time among themselves: it leaves the first data point intact, the second one is averaged with the penultimate, the third with the antepenultimate, and so on until the last data point, which is also left intact. It creates CSVs for these new averages and stores them in the folder 'final'.
#The final interest is the folder called 'final' which contains the C(t) coefficients needed to plot with the file 'Analysis.py'.


#IT IS NECESSARY TO ALTER THE PATHS MENTIONED HERE, AS THEY DEPEND ON WHERE THE FILES ARE LOCATED ON EACH COMPUTER.
#pa variable iterates to create directories where each package of momenta are stored (0 0 P_z, -1 0 P_z, 1 0 P_z, etc.)
pa = 0
while pa < 41:
    # Initial file path template
    file_path_template = 'C:/Users/PC/Downloads/REYES/Data/pion_P4/pion_P4/{}'
    
    # Output directory
    output_directory = 'C:/Users/PC/Downloads/REYES/Data/pion_P4/Averaged'
    os.makedirs(output_directory, exist_ok=True)
    
    # Range of directories to process
    directories = range(0, 2400, 2)
    
    # Initialize an empty list to hold the resulting arrays for each directory
    results = []
    last_data_length = None
    
    for dir_number in directories:
        directory_path = file_path_template.format(dir_number)
        
        file_path1 = directory_path + '/twop_momforsmear_+0_+0_+4_zeta_-0.8000_dir_z.dat'
        file_path2 = directory_path + '/twop_momforsmear_+0_+0_-4_zeta_-0.8000_dir_z.dat'
        
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
                #This is because directories 862 and 1196 are empty and errors kept poping, get fixed, error >:D
            continue
    
        # Ensures that both files have the same length
        if data1.shape != data2.shape:
            print(f"Files in directory {directory_path} have different shapes.")
            continue
    
        # This averages the data
        combined_data = (data1 + data2) / 2
    
        # Appends the result to the list
        results.append(combined_data)
    
        # Save the averaged data to a CSV file
        output_file_path = os.path.join(output_directory, f'{dir_number}.csv')
        np.savetxt(output_file_path, combined_data, delimiter=',')
        
        print(f"Processed and saved directory: {directory_path}")
    
    print("Processing complete. Averaged files have been saved.")
    
    #Remember to change the directories names if you change momenta (P2 or P4) in the whole code
    input_dir = 'C:/Users/PC/Downloads/REYES/Data/pion_P4/Averaged'
    output_dir = f'C:/Users/PC/Downloads/REYES/Data/pion_P4/Averaged/analysis/{pa}'
    
    # Ensures the output directory exists. This is such a stupid mistake, get fixed aswell >:D
    os.makedirs(output_dir, exist_ok=True)
    
    
    # Variable to determine which group of 64 rows to process
    grupo = pa + 1  # Modify this variable to choose which group of 64 rows to process (1 for first 64 rows, 2 for second 64 rows, etc.)
    
    # Loop through all the files in the input directory
    for file_name in os.listdir(input_dir):
        input_file_path = os.path.join(input_dir, file_name)
        
        # Check if the file is a CSV file
        if os.path.isfile(input_file_path) and input_file_path.endswith('.csv'):
            # Calculates the starting row for the group
            start_row = (grupo - 1) * 64
            end_row = start_row + 64
    
            try:
                # Reads the specific group of 64 rows
                df = pd.read_csv(input_file_path, skiprows=start_row, nrows=64)
                
                # Defines the output file path
                output_file_path = os.path.join(output_dir, file_name)
                
                # Saves the selected rows to a new CSV file
                df.to_csv(output_file_path, index=False)
                
                print(f'Saved rows {start_row + 1} to {end_row} of {file_name} to {output_file_path}')
            except pd.errors.EmptyDataError:
                print(f'File {file_name} does not have enough rows for group {grupo}. Skipping.')
    
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
        file_paths.append(f'C:/Users/PC/Downloads/REYES/Data/pion_P4/Averaged/analysis/{pa}/' + f'{index}.csv')
    
    # Process each file and store results in separate lists
    final_lists = []
    output_dir1 = f'C:/Users/PC/Downloads/REYES/Data/pion_P4/Averaged/analysis/{pa}/final'
    os.makedirs(output_dir1, exist_ok=True)
    
    for idx, file_path in enumerate(file_paths):
        final_list = process_file(file_path)
        final_lists.append(final_list)
        print(f"Final list {idx}: {final_list}")
    
    # Optionally, save the final lists to new CSV files
    for idx, final_list in enumerate(final_lists):
        output_path = f'C:/Users/PC/Downloads/REYES/Data/pion_P4/Averaged/analysis/{pa}/final/' + f"{idx}.csv"
        pd.DataFrame(final_list).to_csv(output_path, index=False, header=False)
    
    pa = pa+1

print(datetime.now() - startTime)