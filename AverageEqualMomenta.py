import os
import pandas as pd

#This code works only after Data_treating2.py and before Analysis.py
#It selects a group of momenta from directories

def average_csv_files(base_dir, indices):
    # Create the result directory if it doesn't exist
    result_dir = os.path.join(base_dir, 'result')
    os.makedirs(result_dir, exist_ok=True)
    
    # Get the list of all files from the first 'final' directory to initialize
    initial_dir = os.path.join(base_dir, str(indices[0]), 'final')
    files = os.listdir(initial_dir)
    
    for file_name in files:
        data_list = []
        
        for index in indices:
            file_path = os.path.join(base_dir, str(index), 'final', file_name)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path, header=None)
                data_list.append(df)
            else:
                print(f"File {file_path} does not exist.")
        
        # Averaging the dataframes
        if data_list:
            avg_df = sum(data_list) / len(data_list)
            
            # Write the averaged data to the new result directory
            result_file_path = os.path.join(result_dir, file_name)
            avg_df.to_csv(result_file_path, header=False, index=False)
            print(f"Averaged data for {file_name} written to {result_file_path}")


base_dir = 'C:/Users/PC/Downloads/REYES/Data/pion_P4/Averaged/analysis'
indices = [37, 38, 39, 40]  # Replace with the desired directory indices

average_csv_files(base_dir, indices)
