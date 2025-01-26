import cv2
import numpy as np

# Step 1: Load the matrix (nav_map.npy)
nav_map = np.load('/Users/anniegouchee/git/uncrashout/src/constants/nav_map.npy')

# Step 2: Load the image with red dots
image_with_dots = cv2.imread('image_with_dots.jpg')

# Convert the image to RGB (OpenCV loads images in BGR)
image_with_dots_rgb = cv2.cvtColor(image_with_dots, cv2.COLOR_BGR2RGB)

# Step 3: Identify red dots in the image (pure red: RGB = (255, 0, 0))
red_pixels = np.where((image_with_dots_rgb[:, :, 0] == 255) & (image_with_dots_rgb[:, :, 1] == 0) & (image_with_dots_rgb[:, :, 2] == 0))

# The coordinates of the red dots (y, x)
red_coords = list(zip(red_pixels[0], red_pixels[1]))

# Step 4: Optionally, handle scaling if the image is resized
# Assuming image_with_dots is a scaled version of the matrix, for example:
scale_factor = 2  # Adjust this based on your actual scaling

# Step 5: Adjust coordinates based on scale
relative_coords = [(int(y * scale_factor), int(x * scale_factor)) for y, x in red_coords]

# Step 6: Map the relative coordinates to the matrix
valid_coords = [coord for coord in relative_coords if 0 <= coord[0] < nav_map.shape[0] and 0 <= coord[1] < nav_map.shape[1]]

# Step 7: Mark the red dots on the nav_map
# Assuming you want to mark them as '255' (red)
for y, x in valid_coords:
    nav_map[y, x] = 255  # Marking the position with a value (e.g., 255)

# Step 8: Save the marked matrix to a new .npy file
np.save('/Users/anniegouchee/git/uncrashout/src/constants/nav_map_marked.npy', nav_map)

# Print the updated matrix (optional)
print("Marked nav_map has been saved as 'nav_map_marked.npy'")
