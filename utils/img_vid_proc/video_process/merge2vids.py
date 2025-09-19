from moviepy import VideoFileClip, concatenate_videoclips

# Load MKV files
clip1 = VideoFileClip("C:\\local_store\\files\\my_workspace\\part1.mkv")
clip2 = VideoFileClip("C:\\local_store\\files\\my_workspace\\part2.mkv")

# Ensure same size and fps
clip2 = clip2.resized(clip1.size).with_fps(clip1.fps)

# Concatenate
final = concatenate_videoclips([clip1, clip2])

# Write to MKV output
final.write_videofile("output.mkv", codec="libx264", audio_codec="aac")
