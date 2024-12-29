import os
import re
from glob import glob

def process_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

    # Regular expression to match the Ranges sections
    pattern = re.compile(
        r'if \(Ranges == 0\)\s*\{\s*'
        r'item \(FEAT_AIRCRAFT, (\w+)\)\s*\{\s*'
        r'property\s*\{\s*range: (\d+); \}\s*\}\s*\}\s*'
        r'if \(Ranges == 1\)\s*\{\s*'
        r'item \(FEAT_AIRCRAFT, \1\)\s*\{\s*'
        r'property\s*\{\s*range: (.*?); \}\s*\}\s*\}\s*'
        r'if \(Ranges == 2\)\s*\{\s*'
        r'item \(FEAT_AIRCRAFT, \1\)\s*\{\s*'
        r'property\s*\{\s*range: (\d+); \}\s*\}\s*\}', 
        re.DOTALL
    )

    def replacement(match):
        aircraft_name = match.group(1)
        range_0 = match.group(2)
        range_1 = match.group(3)
        range_2 = match.group(4)

        return (
            f"switch (FEAT_AIRCRAFT, SELF, sw_{aircraft_name}_range, Ranges) {{\n"
            f"    0: return {range_0};\n"
            f"    1: return {range_1};\n"
            f"    2: return {range_2};\n"
            f"    default: return 0; // Fallback for unexpected values\n"
            f"}}"
        )

    # Perform the replacement
    updated_content = pattern.sub(replacement, content)

    # Write back the changes to the file
    with open(filepath, 'w') as file:
        file.write(updated_content)

    print(f"Processed {filepath}")

def process_pnml_files(directory):
    # Use glob to find all .pnml files recursively
    pnml_files = glob(os.path.join(directory, '**/*.pnml'), recursive=True)
    for filepath in pnml_files:
        process_file(filepath)

# Specify the directory containing .pnml files
directory = './src'
process_pnml_files(directory)

