import os
import shutil

import praw
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import time
import io
from selenium.webdriver.support.wait import WebDriverWait
###
# NOTE
# Delete from here the selenium folder and then run it 2 times
# C:\Users\matei\.cache
###
class Comment:
    def __init__(self, author, body):
        self.author = author
        self.body = body
        self.char_count = len(body)
        self.screentime = self.get_screentime_in_sec()
        self.crop_factor_width = self.get_crop_factor()
        self.new_lines_count = self.get_newline_count()
        self.filename= f"{author}_{self.char_count}.png"

    def get_crop_factor(self):
        if self.char_count< 100:
            if self.char_count <= 50:
                return 50
            return self.char_count / 100
        else:
            return 100

    def get_newline_count(self):
        new_lines = self.char_count - self.body.count('\n') * 100
        if new_lines < 0:
            return self.body.count('\n') * 100
        return new_lines // 100

    def get_screentime_in_sec(self):
        # Assuming 2 second per 100 characters
        return max(2, self.char_count*2 // 100)

#todo background video no copyright https://www.youtube.com/results?search_query=no+copyright+phone+gameplay
# todo add no copyright music to the video https://www.youtube.com/results?search_query=no+copyright+tiktok+music
# todo list of links and comments to be used
# todo schdeuler: note when a video has been posted and post if not posted in that day
# todo post it with https://pypi.org/project/tiktok-uploader/
# todo or this but i'm unsure https://github.com/davidteather/TikTok-Api
#description:
#redditdaily #minecraftparkour #reddit #redditstories #redditreadings #askreddit #fyp #askreddit #crazytales #mindblown #nsfw #storytime #communitystories #tiktokdiscoveries #questioneverything
# #redditdaily #minecraftparkour #reddit #redditstories #redditreadings #askreddit #fyp #askreddit #crazytales #mindblown #nsfw #storytime #communitystories #tiktokdiscoveries #questioneverything
# ========== SETUP ========== #
#https://www.tiktok.com/@reno_onet/video/7501760888278420758?lang=en

REDDIT_URL = "https://www.reddit.com/r/AskReddit/comments/1khdjyi/whats_the_stupidest_thing_the_most_intelligent/"
NUM_COMMENTS = 3
NEW_LINE_HEIGHT_PX=18 # height of a new line in a comments i pixels
SIMPLE_POST_HEIGHT_PX=104 # height of a simple post with a single line in pixels
FIRST_N_COMMENTS = 100 # number of comments to scrape
reddit = praw.Reddit (
    username= "Life_Reindeer_4581",
    password= "valoare444",
    client_id="W4hrI-z8O_wJXG4JM5cXdQ",
    client_secret="Knyd7t4BdZ_GkoX8O-JpG1ej7urlYg",
    user_agent="Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
)




# ========== SCRAPE TOP COMMENTS ========== #
comments_obj: list[Comment] = []

def resize_png_to_width(path: str, output_path: str, target_width: int = 607):
    image = Image.open(path)

    aspect_ratio = image.height / image.width
    new_height = int(target_width * aspect_ratio)
    resized_image = image.resize((target_width, new_height), Image.LANCZOS)
    resized_image.save(output_path)


def get_screenshots(REDDIT_URL):
    global comments_obj
    submission = reddit.submission(url=REDDIT_URL)
    submission.comment_sort = 'top'
    submission.comments.replace_more(limit=0)

    comments_count = len(submission.comments)
    if comments_count < NUM_COMMENTS:
        print(f"❌ Not enough comments. Found {comments_count} comments.")
        exit()

    top_comments_non_deleted = []#submission.comments[:NUM_COMMENTS]
    for idx,comment in enumerate(submission.comments[:FIRST_N_COMMENTS]):
        if comment.author:
            top_comments_non_deleted.append(comment)
        else:
            continue

    top_comments = top_comments_non_deleted[:NUM_COMMENTS]
    for idx,comment in enumerate(top_comments):
        author_name = comment.author.name if comment.author else "deleted"
        if author_name == "deleted":
            pass

        comment_obj= Comment(author_name, comment.body)
        comments_obj.append(comment_obj)
        #newline_count = comment.body.count('\n')


        print(f"Comment {idx} by u/{comment_obj.author} (Score: {comment.score}):\n{comment.body}")
        print(f"Newlines: {comment_obj.new_lines_count}")
        print('-' * 80)

    print(comments_obj[0])

    # Setup headless browser
    options = Options()
    options.headless = False
    #options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome(options=options)
    #driver.maximize_window()
    driver.set_window_size(600, 800)
    driver.get(REDDIT_URL)

    try:
        wait = WebDriverWait(driver, 5)
        comment_element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f'shreddit-post')
        ))

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment_element)
        time.sleep(1)
        png = comment_element.screenshot_as_png
        image = Image.open(io.BytesIO(png))

        os.makedirs("files_new/title", exist_ok=True)
        image.save(f"files_new/title/title.png")
        resize_png_to_width(f"files_new/title/title.png",f"files_new/title/title.png")
        print(f"✅ Saved title.png")

        for index,comment in enumerate(comments_obj):
            comment_element = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, f'shreddit-comment[author="{comment.author}"]')
            ))

            # Scroll to the element
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment_element)
            time.sleep(1)

            # Screenshot the element
            png = comment_element.screenshot_as_png
            image = Image.open(io.BytesIO(png))

            # Crop to top 100px
            width, height = image.size
            cropped = image.crop((10, 0, width, min(SIMPLE_POST_HEIGHT_PX + comment.new_lines_count * NEW_LINE_HEIGHT_PX, height)))
            comment.filename = f"comment{index}.png"
            os.makedirs("files_new/images", exist_ok=True)  # Ensure directory exists
            cropped.save("files_new/images/"+comment.filename)
            resize_png_to_width("files_new/images/"+comment.filename,"files_new/images/"+comment.filename)
            print(f"✅ Saved cropped_comment{index}.png")

    except Exception as e:
        print("❌ Element not found or timed out:", e)

    driver.quit()

def move_all_to_folder(src_folder: str, dst_folder: str):
    """Moves all contents from src_folder to dst_folder."""
    os.makedirs(dst_folder, exist_ok=True)  # Ensure destination exists
    for filename in os.listdir(src_folder):
        src_path = os.path.join(src_folder, filename)
        dst_path = os.path.join(dst_folder, filename)
        try:
            shutil.move(src_path, dst_path)
        except Exception as e:
            print(f"Failed to move {src_path}. Reason: {e}")


from misc import random_generator
move_all_to_folder("files_new", f"{random_generator.generate_unique_uuid()}")

get_screenshots(REDDIT_URL=REDDIT_URL)

#resize_png_to_width("files_new/title/title.png", "files_new/title/title.png", scale=0.82)

def create_video(video_path):
    global comments_obj
    TITLE_TIME=3
    output_path = "output.mp4"

    # === Load base video ===
    base_video = VideoFileClip(video_path)

    # === Create overlay clips ===
    overlay_clips = []
    time = 0
    img_clip = (
        ImageClip("files_new/title/title.png")
        .with_duration(TITLE_TIME)
        .with_position("center")
        .with_start(time)
    )
    time += TITLE_TIME
    overlay_clips.append(img_clip)
    for idx, comment in enumerate(comments_obj):
        img_clip = (
            ImageClip("files_new/images/"+comment.filename)
            .with_duration(comment.screentime)
            .with_position("center")
            .with_start(time)
        )

        overlay_clips.append(img_clip)
        time += comment.screentime

    # === Combine base video and overlays ===
    final = CompositeVideoClip([base_video] + overlay_clips)
    # === Write output ===
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

video_path = "trimmed_10s.mp4"

create_video(video_path)