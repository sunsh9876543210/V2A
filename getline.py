import cv2
import numpy as np
import math

def find_line_and_tangent(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Image at path {image_path} could not be loaded.")

    # Apply Canny edge detection
    edges = cv2.Canny(image, 50, 150, apertureSize=3)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    
    if lines is not None:
        for rho, theta in lines[:, 0]:
            # Convert polar coordinates (rho, theta) to Cartesian coordinates (x1, y1, x2, y2)
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            # Draw the line on the image (optional)
            line_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.imshow("Detected Line", line_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # Calculate the tangent of the line
            delta_x = x2 - x1
            delta_y = y2 - y1
            if delta_x == 0:
                tangent = float('inf')  # Vertical line
            else:
                tangent = delta_y / delta_x

            return (x1, y1, x2, y2), tangent
    
    raise ValueError("No lines were found in the image.")

# Example usage
image_path = './000026.png'
line_coords, tangent = find_line_and_tangent(image_path)
print(f"Line coordinates: {line_coords}")
print(f"Tangent of the line: {tangent}")