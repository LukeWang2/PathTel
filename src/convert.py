import matplotlib.pyplot as plt
import numpy as np


def save_and_display_array_as_image(array, output_filename):
    """
    Convert a regular 2D array of 0s and 1s to a PNG image and display it.

    Parameters:
        array (list of lists): 2D list with 0s and 1s (0 for floor, 1 for walls).
        output_filename (str): Name of the output PNG file.
    """

    # Create a colormap: white for 0s, black for 1s
    cmap = plt.cm.binary

    # Save the array as an image
    plt.figure(figsize=(len(array[0]) / 10, len(array) / 10), dpi=100)
    plt.imshow(array, cmap=cmap, interpolation="nearest")
    plt.title("Occupancy Map")  # Optional: Add a title
    plt.tight_layout(pad=0)

    # Save to the specified file
    plt.savefig(output_filename, bbox_inches="tight", pad_inches=0)
    plt.close()

    # Display the image
    plt.imshow(array, cmap=cmap, interpolation="nearest")
    plt.axis("on")  # Ensure axes are displayed when showing
    plt.xticks(ticks=range(0, array.shape[1], 100))  # Set x-ticks for display
    plt.yticks(ticks=range(array.shape[0], 0, -100))  # Set y-ticks for display
    plt.title("Occupancy Map")  # Optional: Add a title
    plt.show()


save_and_display_array_as_image(
    np.load("/Users/lukewang/Coding/Hackathons/uncrashout/src/constants/nav_map.npy"),
    "test.png",
)
