import os
import re
from glob import glob

def process_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

    # Match the `switch` block
    switch_pattern = re.compile(r'switch \(FEAT_AIRCRAFT, SELF, sw_(\w+)_range, Ranges\) \{.*?\}', re.DOTALL)
    switch_match = switch_pattern.search(content)

    # Match the `item` block
    item_pattern = re.compile(
        r'item \(FEAT_AIRCRAFT, (\w+)\)\s*\{.*?\s*graphics\s*\{.*?\}\s*\}', re.DOTALL
    )
    item_match = item_pattern.search(content)

    # Ensure both sections are found
    if not switch_match or not item_match:
        print(f"Skipping {filepath}: Required sections not found.")
        return

    # Extract the sections
    switch_section = switch_match.group()
    item_section = item_match.group()

    # Remove these sections from the content
    updated_content = content.replace(switch_section, '').replace(item_section, '')

    # Append the sections to the end of the file
    updated_content = updated_content.strip() + "\n\n" + switch_section + "\n\n" + item_section

    # Write the updated content back to the file
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

