import cv2
import numpy as np

# Example matrix of image (assuming it's in the form of a NumPy array)
image_matrix = cv2.imread('image_matrix.jpg')  # This is your matrix representation of the image

# Load the image with red dots (image where dots are drawn)
image_with_dots = cv2.imread('image_with_dots.jpg')

# Convert the image with dots to RGB if needed (OpenCV loads images in BGR by default)
image_with_dots = cv2.cvtColor(image_with_dots, cv2.COLOR_BGR2RGB)

# Find red pixels (pure red: RGB = (255, 0, 0))
red_pixels = np.where((image_with_dots[:, :, 0] == 255) & (image_with_dots[:, :, 1] == 0) & (image_with_dots[:, :, 2] == 0))

# red_pixels will be a tuple (rows, cols), i.e., (y, x) coordinates
red_coords = list(zip(red_pixels[0], red_pixels[1]))

# If you have a transformation factor (e.g., image_with_dots is a scaled version of image_matrix):
# Example: scale factor for resizing
scale_factor = 2  # assuming image_with_dots is half the size of image_matrix

# Adjust coordinates based on scale factor
relative_coords = [(int(y * scale_factor), int(x * scale_factor)) for y, x in red_coords]

# Print the relative coordinates
print("Relative positions of red dots in matrix:", relative_coords)
