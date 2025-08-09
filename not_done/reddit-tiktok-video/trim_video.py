#TRIM VIDEO
from moviepy import VideoFileClip

def trim_video(path, start=0, end=30):
    output_path = f"trimmed_{end}s.mp4"
    video = VideoFileClip(path).subclipped(0, end)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

trim_video("cropped_output_video.mp4",0,10)