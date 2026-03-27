import cv2
from util import get_limits
from util import get_color_name
import time

# Input color in BGR format
what_color = [0, 0, 0]
what_color[0] = int(input("Blue = "))
what_color[1] = int(input("Green = "))
what_color[2] = int(input("Red = "))

# Initialize global variables for mouse click position and time tracking
clicked_position = None
last_click_time = None
display_duration = 10  # Duration to display the color code after clicking

def mouse_callback(event, x, y, flags, param):
    global clicked_position, last_click_time
    if event == cv2.EVENT_LBUTTONDOWN:  # Capture left mouse click position
        clicked_position = (x, y)
        last_click_time = time.time()  # Update last click time

cap = cv2.VideoCapture(0)  # Initialize video capture
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', mouse_callback)  # Set mouse callback for the window

while True:
    ret, frame = cap.read()  # Read a frame from the camera
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert to HSV color space

    lowerLimit, upperLimit = get_limits(color=what_color)  # Get HSV limits
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)  # Create a mask for the specified color

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Flag to check if any object is detected
    object_detected = False

    # Draw bounding boxes around detected contours
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Filter out small contours
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            object_detected = True

    if object_detected:
        color_name = get_color_name(what_color)  # Get the color name for display
        cv2.putText(frame, color_name, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    cv2.putText(frame, "Press Q to quit.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display color code and follow clicked point
    if clicked_position:
        current_time = time.time()
        if current_time - last_click_time < display_duration:
            x, y = clicked_position
            if x >= 0 and y >= 0 and x < frame.shape[1] and y < frame.shape[0]:
                # Get the color at the clicked position
                color_bgr = frame[y, x]
                color_rgb = (color_bgr[2], color_bgr[1], color_bgr[0])  # Convert BGR to RGB
                color_text = f'RGB: {color_rgb}'
                cv2.putText(frame, color_text, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                # Draw a circle at the clicked position for better visibility
                cv2.circle(frame, (x, y), 5, (0, 255, 255), -1)
        else:
            clicked_position = None  # Clear position after display duration

    cv2.imshow('frame', frame)  # Show the video frame

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit on 'Q' key press
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close all OpenCV windows