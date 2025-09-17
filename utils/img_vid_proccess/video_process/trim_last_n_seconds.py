from moviepy import VideoFileClip

# Load your video
input_path = "C:\\local_store\\files\\my_workspace\\video_process\\input.mkv"
output_path = "C:\\local_store\\files\\my_workspace\\video_process\\trimmed_video.mkv"

# Load the clip
clip = VideoFileClip(input_path)

# Calculate new duration (original duration - 10 seconds)
new_duration = max(0, clip.duration - 10)

# Trim and save the video
trimmed_clip = clip.subclipped(0, new_duration)
trimmed_clip.write_videofile(output_path, codec="libx264")
#BAP_R7 SWE.3 Part1