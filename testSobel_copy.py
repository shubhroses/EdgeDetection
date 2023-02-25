# import modules
import arcpy
import rasterio
from rasterio.plot import show
import numpy as np
from scipy import ndimage
# set environment
#aprx = arcpy.mp.ArcGISProject("CURRENT")
arcpy.env.workspace = "C:/BDCC Map"

def get_important_pixels(image_file, num_pixels):
    # Load the image file using rasterio
    with rasterio.open(image_file) as dataset:
        # Read the image data into a numpy array
        image_data = dataset.read()

    # Convert the image to grayscale
    image_gray = np.mean(image_data, axis=0);


    # Apply the Sobel operator to detect edges
    dx = ndimage.sobel(image_gray, 0)
    dy = ndimage.sobel(image_gray, 1)
    edge = np.sqrt(dx ** 2 + dy ** 2)

    # Get the coordinates of the num_pixels most important pixels
    coords = np.argpartition(edge.flatten(), -num_pixels)[-num_pixels:]
    y_coords, x_coords = np.unravel_index(coords, edge.shape)

    # Return the coordinates as a list of tuples
    return list(zip(x_coords, y_coords))

## Recommend file entry as input for arcgis tool.
img = "maxresdefault.jpg";
important_pixels = get_important_pixels(img, 1000)
print(important_pixels)

print("Script completed")
