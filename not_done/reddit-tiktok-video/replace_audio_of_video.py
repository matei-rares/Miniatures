import ffmpeg
from moviepy import VideoFileClip, AudioFileClip

input_video = r"D:\aaaa\git\Miniatures\misc\trimmed_61.mp4"
input_audio = r"D:\aaaa\git\Miniatures\misc\background_music.mp3"
output_video = r"D:\aaaa\git\Miniatures\misc\output_video.mp4"
# video = VideoFileClip("trimmed_61.mp4")
# audio = AudioFileClip("background_music.mp3")
#
# # Set the new audio to the video
# final_video = video.with_audio(audio)
#
# # Export the result
# final_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")

# Usage
def set_custom_audio_to_video(video_path: str, audio_path: str, output_path: str):
    # Load the video and audio files
    video = VideoFileClip(video_path)
    video_duration = video.duration

    # Load the audio and start it from 18 seconds
    audio = AudioFileClip(audio_path).subclipped(18)

    # Trim or extend the audio to match the video duration
    audio = audio.subclipped(0, min(audio.duration, video_duration))

    # Set the new audio
    final_video = video.with_audio(audio)

    # Write the result to file
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage
set_custom_audio_to_video(input_video,input_audio, output_video)