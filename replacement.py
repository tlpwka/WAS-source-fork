import os
import re
from glob import glob

def process_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    inside_target_section = False

    for line in lines:
        # Check if we are entering the target section
        if "if (Ranges == 1)" in line:
            inside_target_section = True
        elif line.strip().startswith("if (Ranges") and "if (Ranges == 1)" not in line:
            inside_target_section = False

        # If inside the target section, look for the range line
        if inside_target_section:
            match = re.search(r'range: (\d+);', line)
            if match:
                range_value = int(match.group(1))
                if range_value < 600:
                    # Append 600*RangeMultipl*RangeMultiplSmallAdd to the range line
                    updated_line = re.sub(r'range: (\d+);', f'range: 600*RangeMultipl*RangeMultiplSmallAdd/10000;', line)
                    updated_lines.append(updated_line)
                elif range_value < 1050:
                    # Append *RangeMultipl*RangeMultiplSmallAdd to the range line
                    updated_line = re.sub(r'range: (\d+);', f'range: {range_value}*RangeMultipl*RangeMultiplSmallAdd/10000;', line)
                    updated_lines.append(updated_line)
                else:
                	updated_line = re.sub(r'range: (\d+);', f'range: {range_value}*RangeMultipl/100;', line)
                	updated_lines.append(updated_line) 
                continue

        updated_lines.append(line)

    # Write back the changes to the file
    with open(filepath, 'w') as file:
        file.writelines(updated_lines)

def process_pnml_files(directory):
    # Use glob to find all .pnml files recursively
    pnml_files = glob(os.path.join(directory, '**/*.pnml'), recursive=True)
    for filepath in pnml_files:
        process_file(filepath)
        print(f"Processed {filepath}")

# Specify the directory containing .pnml files
directory = './src'
process_pnml_files(directory)

