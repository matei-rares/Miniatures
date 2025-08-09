import pyautogui
import cv2
import numpy as np
from PIL import Image
import os
#todo use locateOnScreen, it return coordinates, give the coordinates to center() and then click()
#make a template for click wait click wait
pyautogui.locateOnScreen('template.png')

# Function to find and click the specific text (template) on the screen
def click_text_on_screen(template_image_path):
    # Check if the template image file exists
    if not os.path.exists(template_image_path):
        print(f"Error: The template file at {template_image_path} was not found.")
        return False

    # Take a screenshot of the whole screen
    screen_image = pyautogui.screenshot()

    # Convert screenshot to numpy array (PIL to numpy)
    screen_np = np.array(screen_image)

    # Convert the screenshot from RGB to BGR (for OpenCV)
    screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

    # Convert the screenshot to grayscale
    screen_gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)

    # Load the template image (the image of the text to find) and convert it to grayscale
    template = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)

    # Ensure the template is smaller than the screen capture
    if template.shape[0] > screen_gray.shape[0] or template.shape[1] > screen_gray.shape[1]:
        print(f"Error: The template is larger than the screen capture. Resize the template.")
        return False

    # Perform template matching to find the text on the screen
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Confidence threshold for matching
    locations = np.where(result >= threshold)

    # If a match is found, click on the center of the matched region
    if len(locations[0]) > 0:
        print(f"Found the text! Clicking on it...")

        # Get the top-left corner of the matched region
        top_left = (locations[1][0], locations[0][0])

        # Get the dimensions of the template (text image)
        h, w = template.shape

        # Calculate the center of the matched region
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2

        # Move the mouse and click at the center of the matched region
        pyautogui.click(center_x, center_y)
        return True

    print(f"Text not found on screen.")
    return False

# Example usage
template_image_path = "template.png"  # Replace with the path to your template image (the text image)
if click_text_on_screen(template_image_path):
    print("Successfully clicked on the text!")
else:
    print("Text was not found.")
