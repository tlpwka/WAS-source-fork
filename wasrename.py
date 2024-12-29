import os
import re

# Define the root folder where the search will begin
root_folder = './src'

# Define the regular expression pattern to match the "conflicted" part
pattern = r' \(conflicted [^\)]+ \d+\)'

# Function to rename files in a directory and its subdirectories
def rename_files_in_directory(directory):
    # Walk through the directory and subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            # Check if the file name matches the pattern
            print(f"Checking file: {file}")  # Debugging: Show each file being checked
            
            new_name = re.sub(pattern, '', file)  # Replace matched part with an empty string
            
            if new_name != file:  # Only rename if the filename has been changed
                # Construct full old and new paths
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, new_name)
                
                # Add debug output
                print(f"Renaming: {old_file_path} -> {new_file_path}")
                
                # Try renaming the file
                try:
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed: {old_file_path} -> {new_file_path}")
                except Exception as e:
                    print(f"Error renaming {old_file_path}: {e}")

# Call the function to start renaming files in the 'src' folder
rename_files_in_directory(root_folder)

