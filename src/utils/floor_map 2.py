import cv2
import numpy as np


def save_matrix_to_npy(matrix, file_path):
    np.save(file_path, matrix)


def load_matrix_from_npy(file_path):
    return np.load(file_path)


def save_matrix_as_image(matrix, file_path="matrix.png"):
    """
    Save a matrix as an image file using OpenCV.
    """
    scaled_matrix = (matrix * 255).astype(np.uint8)  # Scale to 0-255
    cv2.imwrite(file_path, scaled_matrix)
    print(f"Matrix saved as {file_path}")


def floorplan_to_matrix(image_path, threshold=128):
    """
    Loads a floor plan (e.g., a blueprint or schematic),
    converts it into a 2D matrix (occupancy grid).

    Returns:
      nav_map: A 2D NumPy array where:
               0 = free space
               1 = obstacle
      display_img: The original image (BGR) for visualization
    """
    # 1. Load the image in grayscale
    gray_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if gray_img is None:
        raise ValueError(f"Cannot load image from {image_path}")

    # 2. Binarize the image using a threshold
    #    Everything above 'threshold' = white (free),
    #    everything below 'threshold' = black (obstacle).
    _, bin_img = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY)

    # 3. Convert to occupancy: 0 = free, 1 = obstacle
    nav_map = np.where(bin_img == 255, 0, 1).astype(np.uint8)

    # Also return a BGR version of original for display
    display_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)

    return nav_map, display_img


mat = floorplan_to_matrix("Screenshot 2025-01-25 at 21.01.33.png")[0]
save_matrix_to_npy(mat, "test.npy")
save_matrix_as_image(mat, "test.png")
