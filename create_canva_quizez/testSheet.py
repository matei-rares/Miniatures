
import cv2
import numpy as np

import os
import pygetwindow as gw
import pyautogui
import time

ABSOLUTE_PATH = os.path.abspath(os.getcwd()) #must be system32
#5 quizez - 12 sec -

def focus_tab():
    windows = gw.getWindowsWithTitle('Google Chrome')
    target_window = None
    for win in windows:
        if win.title.endswith('Google Chrome'):
            target_window = win
            break

    if target_window:
        target_window.activate()
        time.sleep(0.1)  # Give it a moment to come to the front
       #todo target_window.maximize()  # Optional: maximize if minimized
        print(f"Focused: {target_window.title}")
    else:
        print("No matching Google Chrome window found.")
##############################################3

focus_tab()
def process_image(template_image_path):
    if not os.path.exists(template_image_path):
        print(f"Error: The template file at {template_image_path} was not found.")
        return False
    screen_image = pyautogui.screenshot()
    screen_np = np.array(screen_image)
    screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
    screen_gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)
    # Ensure the template is smaller than the screen capture
    if template.shape[0] > screen_gray.shape[0] or template.shape[1] > screen_gray.shape[1]:
        print(f"Error: The template is larger than the screen capture. Resize the template.")
        return False
    # Perform template matching to find the text on the screen
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Confidence threshold for matching
    locations = np.where(result >= threshold)
    print(f"Found {len(locations[0])} matches with confidence >= {threshold}.")
    for i in range(len(locations[0])):
        print(f"Match {i + 1}: Location: ({locations[1][i]}, {locations[0][i]})")
    is_results_found = True
    if len(locations[0]) == 0:
        print(f"Error: No matches found with confidence >= {threshold}.")
        is_results_found = False
    h,w = template.shape
    return locations, h,w, is_results_found

def click_image(template_image_path, click_type ="one", horizontal_template_relative:float =0.5, vertical_template_relative:float =0.5 ):
    print(template_image_path)
    locations,h,w,is_found = process_image(template_image_path)
    while is_found == False:
        print(f"Image {template_image_path} not found. Retrying...")
        time.sleep(0.1)
        locations,h,w,is_found = process_image(template_image_path)
    if len(locations[0]) > 0:
        print(f"Found image location! Clicking on it...")
        top_left = (locations[1][0], locations[0][0])

        center_x = top_left[0] + w * horizontal_template_relative
        center_y = top_left[1] + h * vertical_template_relative

        pyautogui.moveTo(center_x, center_y)
        if click_type == "one":
            pyautogui.click(center_x, center_y)
        elif click_type == "double":
            pyautogui.doubleClick(center_x, center_y)
        else:
            print(f"Error: Invalid click_type value. Use 'one' or 'double'.")
            return False

        return True
    print(f"Text not found on screen.")
    return False
def wait_seconds(n:float=0.1):
    time.sleep(n)

import pyautogui
import pyperclip
import time
def paste(text):
    pyperclip.copy('')          # Wipe it first
    time.sleep(0.05)
    pyperclip.copy(text)
    wait_seconds(0.1)
    pyautogui.hotkey("ctrl", "v")
def select_all():
    pyautogui.hotkey("ctrl", "a")
    wait_seconds(0.1)
def hit_enter():
    pyautogui.press("enter")
BASE_IMG_PATH= '/\\'
CENTER = "center"
center = "center"
DOUBLE = "double"
double = "double"
ONE = "one"
one = "one"

seconds=None
def start_timer():
    global seconds
    seconds = time.time()

def stop_timer():
    global seconds
    elapsed_time = time.time() - seconds
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    seconds = None


CANVA_TEMPLATE_2="https://www.canva.com/design/DAGlTUGJbtk/15weiGpeAbPxzRuIz4Ga0w/edit?ui=eyJEIjp7IlAiOnsiQiI6ZmFsc2V9fX0"
CANVA_TEMPLATE_1="https://www.canva.com/design/DAGmInPgOT8/1cmd7HdZVmOAJqiDj0LWLA/edit"
CANVA_TEMPLATE_3="https://www.canva.com/design/DAGlTX8Aky8/n69tsYa13qOxbxDP4c2jPw/edit?ui=eyJIIjp7IkEiOnRydWV9fQ"

answear_a = "asdfasdf"
answear_b = "asdfasdf"
answear_c = "asdfasdf"
full_answear_a = "A) "+answear_a
full_answear_b = "B) "+answear_b
full_answear_c = "C) "+answear_c
correct_answear = full_answear_b

current_template_link = CANVA_TEMPLATE_2
current_question = "dsfkajsdnfkjasb as dfaksdj akjsb kjasbd kfjasbkj bakjs bdkja bsdf"

def create_quiz():
    click_image(BASE_IMG_PATH + "img_2.png")
    paste(current_template_link) #redirect
    hit_enter()
    wait_seconds(5.5)
    click_image(BASE_IMG_PATH + "img_14.png", click_type=double)
    wait_seconds(0.5)
    #First slide
    click_image(BASE_IMG_PATH + "img_4.png",vertical_template_relative=1.2,click_type=double)
    select_all()
    wait_seconds(0.1)
    print(current_question)
    paste(current_question)

    click_image(BASE_IMG_PATH + "img_5.png",horizontal_template_relative=1,click_type=double)
    select_all()
    wait_seconds(0.1)
    paste(full_answear_a)

    click_image(BASE_IMG_PATH + "img_6.png",horizontal_template_relative=1,click_type=double)
    select_all()
    wait_seconds(0.1)
    paste(full_answear_b)

    click_image(BASE_IMG_PATH + "img_7.png",horizontal_template_relative=1,click_type=double)
    select_all()
    wait_seconds(0.1)
    paste(full_answear_c)

    #Go to second slide
    click_image(BASE_IMG_PATH + "img_8.png",horizontal_template_relative=-0.5,click_type=one)

    #Second slide
    click_image(BASE_IMG_PATH + "img_4.png",vertical_template_relative=1.2,click_type=double)
    select_all()
    wait_seconds(0.1)
    paste(current_question)

    if current_template_link == CANVA_TEMPLATE_1:
        click_image(BASE_IMG_PATH + "img_9.png", horizontal_template_relative=2, click_type=double)
        select_all()
        wait_seconds(0.1)
        paste(full_answear_a)

        click_image(BASE_IMG_PATH + "img_6.png", horizontal_template_relative=1, click_type=double)
        select_all()
        wait_seconds(0.1)
        paste(full_answear_b)

        click_image(BASE_IMG_PATH + "img_7.png", horizontal_template_relative=1, click_type=double)
        select_all()
        wait_seconds(0.1)
        paste(full_answear_c)

    if current_template_link == CANVA_TEMPLATE_2:
        click_image(BASE_IMG_PATH + "img_5.png",horizontal_template_relative=1, click_type=double)
        select_all()
        wait_seconds(0.1)
        paste(full_answear_a)

        click_image(BASE_IMG_PATH + "img_9.png",horizontal_template_relative=2, click_type=double)
        select_all()
        wait_seconds(0.1)
        paste(full_answear_b)

        click_image(BASE_IMG_PATH + "img_7.png",horizontal_template_relative=1, click_type=double)
        select_all()
        wait_seconds(0.1)
        paste(full_answear_c)

    if current_template_link == CANVA_TEMPLATE_3:
        click_image(BASE_IMG_PATH + "img_5.png", horizontal_template_relative=1, click_type=double)
        select_all()
        wait_seconds(0.1)
        paste(full_answear_a)

        click_image(BASE_IMG_PATH + "img_6.png", horizontal_template_relative=1, click_type=double)
        select_all()
        wait_seconds(0.1)
        paste(full_answear_b)

        click_image(BASE_IMG_PATH + "img_9.png", horizontal_template_relative=2, click_type=double)
        select_all()
        wait_seconds(0.1)
        paste(full_answear_c)

def download_quiz():
    click_image(BASE_IMG_PATH + "img_10.png")
    wait_seconds(1)
    click_image(BASE_IMG_PATH + "img_11.png")
    wait_seconds(1.5)
    click_image(BASE_IMG_PATH + "img_12.png")
    wait_seconds(2)
    _,_,_,is_downloading = process_image(BASE_IMG_PATH + "img_13.png")
    print(is_downloading)
    while is_downloading == True:
        _, _, _, is_downloading = process_image(BASE_IMG_PATH + "img_13.png")

create_quiz()
download_quiz()

# current_template_link = CANVA_TEMPLATE_1
# current_question += "1"
# create_quiz_moviepy()
# download_quiz()
#
# current_template_link = CANVA_TEMPLATE_3
# current_question += "3"
# create_quiz_moviepy()
# download_quiz()

wait_seconds(5)




# select_all()
# wait_seconds(0.1)
# paste(current_question)
