from moviepy import VideoFileClip


def crop_center_1920x1080_video_to_phone(input: str, output: str):
    clip = VideoFileClip(input)
    crop_width = 607 # 1080 ^2 / 1920
    crop_height = 1080

    x_center = clip.w / 2
    y_center = clip.h / 2

    x1 = x_center - crop_width / 2
    y1 = y_center - crop_height / 2
    print(clip.w, clip.h)
    print(x_center, y_center)
    print(x1, y1)
    cropped = clip.cropped(x1=x1, y1=y1, x2=x1 + crop_width, y2=y1 + crop_height)
    cropped.write_videofile(output, codec="libx264", audio_codec="aac")

input = "input.mp3"
output = f"cropped_{input}"
crop_center_1920x1080_video_to_phone(input,output)