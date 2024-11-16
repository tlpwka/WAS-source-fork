from PIL import Image
import numpy as np
from scipy.ndimage import label, find_objects

# Step 1: Load the image
image_path = "<path-to-png>"  # Replace this with the path to your image file
image = Image.open(image_path)

# Step 2: Convert the image to a NumPy array for pixel-level analysis
image_array = np.array(image)

# Step 3: Define the blue color in RGB format (assuming pure blue: 0, 0, 255)
blue_color = [0, 0, 255]

# Step 4: Find all pixels matching the blue color
blue_pixels = np.all(image_array[:, :, :3] == blue_color, axis=-1)

# Step 5: Label contiguous blue regions to find individual squares
labeled_array, num_features = label(blue_pixels)

# Print the number of detected features
print(f"Number of detected regions: {num_features}")

# Step 6: Measure properties of labeled regions (bounding boxes for blue squares)
blue_square_slices = find_objects(labeled_array)

# Step 7: Calculate bounding boxes and their coordinates
bounding_boxes = []
for slc in blue_square_slices:
    if slc is not None:
        # Extract bounding box coordinates (min_row, min_col, max_row, max_col)
        min_row, max_row = slc[0].start, slc[0].stop
        min_col, max_col = slc[1].start, slc[1].stop
        bounding_boxes.append((min_col, min_row, max_col - min_col, max_row - min_row))

# Debugging: Print all bounding boxes
print(f"Detected bounding boxes: {bounding_boxes}")

# Step 8: Convert bounding boxes to the requested sprite format
# Format: [frame_index, frame_index, width, height, x_offset, y_offset, ANIM]
sprite_data = []
frame_index = 1  # Start frame index at 1

for bbox in bounding_boxes:
    x, y, width, height = bbox
    x_offset = -width // 2  # Assuming x_offset centers the sprite horizontally
    y_offset = -height // 2  # Assuming y_offset centers the sprite vertically

    # Format the data
    sprite_data.append([frame_index, frame_index, width, height, x_offset, y_offset, "ANIM"])
    frame_index += 1

# Step 9: Display all formatted sprite data entries
print(f"Total sprites detected: {len(sprite_data)}")
print(sprite_data)