import cv2
import numpy as np
import os
import tifffile  # pip install tifffile

# --- Configuration ---
input_path = r'Year_2_I\Bildes\vista-aburrell-195226.jpg'
output_tiff = r'c:\Users\akaletovs\Downloads'
desired_width, desired_height = 100000, 100000
tile_size = 1000  # Process output image in 1000x1000 pixel tiles

# --- Load the input image (assumed to be small enough to fit in memory) ---
img = cv2.imread(input_path, cv2.IMREAD_COLOR)
if img is None:
    raise ValueError(f"Could not load image from {input_path}")
input_height, input_width = img.shape[:2]

# --- Calculate scale factor ---
# We want the output image's largest side to be 100k, while preserving the aspect ratio.
scale_w = desired_width / input_width
scale_h = desired_height / input_height
scale = max(scale_w, scale_h)  # Use the larger factor so that one side reaches the target

new_width = int(input_width * scale)
new_height = int(input_height * scale)
print(f"Input image: {input_width}x{input_height}, scaling factor: {scale:.4f}, "
      f"intermediate size: {new_width}x{new_height}")

# --- Prepare an output memmap ---
# We create a temporary memmap file that will store the huge output image.
# Here we assume an 8-bit 3-channel (RGB) image.
output_shape = (desired_height, desired_width, 3)
memmap_filename = 'output_memmap.dat'
output_memmap = np.memmap(memmap_filename, dtype=np.uint8, mode='w+', shape=output_shape)

# --- Process the output image in tiles ---
# For each tile in the output image, determine the corresponding region in the input image.
# Because we're scaling up, an output coordinate maps to an input coordinate = output / scale.
for y_out in range(0, desired_height, tile_size):
    for x_out in range(0, desired_width, tile_size):
        # Determine tile dimensions (handle edges)
        tile_w = min(tile_size, desired_width - x_out)
        tile_h = min(tile_size, desired_height - y_out)
        
        # Compute the corresponding region in the input image (in float coordinates)
        # Note: Because our overall target (new_width, new_height) might be larger than desired_width/height,
        # we clip to the desired region.
        # Here we assume we want the top-left desired_width x desired_height of the scaled image.
        x0_in = x_out / scale
        y0_in = y_out / scale
        x1_in = (x_out + tile_w) / scale
        y1_in = (y_out + tile_h) / scale
        
        # Determine integer bounds for the input region.
        # We add a pixel margin to account for rounding, if needed.
        x0_in_int = int(np.floor(x0_in))
        y0_in_int = int(np.floor(y0_in))
        x1_in_int = int(np.ceil(x1_in))
        y1_in_int = int(np.ceil(y1_in))
        
        # Crop the input region (be sure not to go out-of-bounds)
        region = img[y0_in_int:min(y1_in_int, input_height),
                     x0_in_int:min(x1_in_int, input_width)]
        
        # Compute the exact size the cropped region would be scaled to.
        # Since cv2.resize expects exact target dimensions, we use (tile_w, tile_h).
        try:
            tile_resized = cv2.resize(region, (tile_w, tile_h), interpolation=cv2.INTER_LANCZOS4)
        except Exception as e:
            print(f"Error resizing tile at ({x_out}, {y_out}) - skipping tile: {e}")
            continue
        
        # Write the tile into the correct location in the memmap.
        output_memmap[y_out:y_out+tile_h, x_out:x_out+tile_w, :] = tile_resized
        
    print(f"Finished processing row starting at y = {y_out}")

# Ensure data is written to disk
output_memmap.flush()
print("All tiles processed and written to memmap.")

# --- Write the memmap to a TIFF file ---
# Using tifffile, we can write the data on disk to a TIFF.
# Note: Writing such a huge file may take a long time.
print("Writing final TIFF file...")
tifffile.imwrite(output_tiff, output_memmap, tile=(tile_size, tile_size))
print(f"Final TIFF saved as {output_tiff}")

# Optionally, remove the temporary memmap file
os.remove(memmap_filename)
