import numpy as np
import cv2

def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    
    hue = hsvC[0][0][0]  # Get the hue value
    saturation = hsvC[0][0][1]  # Get the saturation value
    value = hsvC[0][0][2]  # Get the brightness value

    # Handle black detection
    if value < 50:
        lowerLimit = np.array([0, 0, 0], dtype=np.uint8)
        upperLimit = np.array([180, 255, 50], dtype=np.uint8)
    
    # Handle white detection
    elif saturation < 50 and value > 200:
        lowerLimit = np.array([0, 0, 200], dtype=np.uint8)
        upperLimit = np.array([180, 50, 255], dtype=np.uint8)
    
    # Handle red hue wrap-around and other colors
    elif hue >= 165 or hue <= 15:
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([max(0, hue - 10), 50, 50], dtype=np.uint8)
        upperLimit = np.array([min(179, hue + 10), 255, 255], dtype=np.uint8)
    print(lowerLimit, upperLimit)
    return lowerLimit, upperLimit

# Handle color name detection
def get_color_name(bgr_color):
    b, g, r = bgr_color[0], bgr_color[1], bgr_color[2]

    if b < 50 and g < 50 and r < 50:
        return "Black"
    elif b > 200 and g > 200 and r > 200:
        return "White"
    elif r > 150 and g < 100 and b < 100:
        return "Red"
    elif g > 100 and r < 200 and b < 200:
        return "Green"
    elif b > 150 and r < 100 and g < 100:
        return "Blue"
    elif r > 150 and g > 100 and b < 100:
        return "Orange"
    elif r > 150 and g > 150 and b < 100:
        return "Yellow"
    else:
        return "Unknown Color"
