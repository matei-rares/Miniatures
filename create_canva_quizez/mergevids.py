import moviepy
import os
from pathlib import Path
from datetime import datetime

from moviepy import VideoFileClip, concatenate_videoclips


def get_recent_files(folder_path, count=3):
    folder = Path(folder_path)
    files = [f for f in folder.iterdir() if f.is_file()]
    # Sort by modified time, descending
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    # Return full paths of the most recent files
    return [str(f.resolve()) for f in files[:count]]

# Example usage:
folder_path = "C:\\Users\\matei\\Downloads"
recent_files = get_recent_files(folder_path)
print(recent_files)

# Use absolute paths
clip1 = VideoFileClip(recent_files[0])
clip2 = VideoFileClip(recent_files[1])
clip3 = VideoFileClip(recent_files[2])

final_clip = concatenate_videoclips([clip1, clip2, clip3])
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

final_clip.write_videofile(f"C:\\Users\\matei\\Downloads\\output{timestamp}.mp4")
print("done")