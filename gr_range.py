import os
import re
from glob import glob

def insert_range_in_graphics(content, aircraft_name):
    # Match the graphics section within the item block
    graphics_pattern = re.compile(
        rf'item \(FEAT_AIRCRAFT, {aircraft_name}\)\s*\{{(.*?)\s*graphics\s*\{{(.*?)\}}(.*?)\}}',
        re.DOTALL
    )

    # Find all item blocks that match the aircraft name
    item_matches = graphics_pattern.findall(content)

    if not item_matches:
        print(f"No matching item found for {aircraft_name}")
        return content

    # Process each match
    for item in item_matches:
        # Check if 'range' line is already present in the graphics section
        graphics_section = item[1]
        if f'range: sw_{aircraft_name}_range();' not in graphics_section:
            # If not, insert the line in the graphics section
            new_graphics_section = graphics_section.strip() + '\n    range: ' + f'sw_{aircraft_name}_range();'
            content = content.replace(graphics_section, new_graphics_section)

    return content

def process_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

    # Extract the aircraft name (e.g., Airbus_A318) from the item blocks and insert the range line into the graphics section
    aircraft_names = re.findall(r'item \(FEAT_AIRCRAFT, (\w+)\)', content)

    if not aircraft_names:
        print(f"No aircraft found in {filepath}.")
        return

    for aircraft_name in set(aircraft_names):  # Iterate through unique aircraft names
        print(f"Processing {aircraft_name} in {filepath}")
        content = insert_range_in_graphics(content, aircraft_name)

    # Write the modified content back to the file
    with open(filepath, 'w') as file:
        file.write(content)

    print(f"Processed {filepath}")

def process_pnml_files(directory):
    # Use glob to find all .pnml files recursively
    pnml_files = glob(os.path.join(directory, '**/*.pnml'), recursive=True)
    for filepath in pnml_files:
        process_file(filepath)

# Specify the directory containing .pnml files
directory = './src'  # Change this to your directory if needed
process_pnml_files(directory)

