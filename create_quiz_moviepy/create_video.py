from moviepy import *
import moviepy
from moviepy.video.tools import *

from PIL import ImageFont
import random
from gtts import gTTS
import os

# # Generate a quiz (simplified for this demo)
# def generate_quiz():
#     question = "What comes next?\n2, 4, 8, 16, ___"
#     options = ["18", "32", "24", "20"]
#     correct = "32"
#     return question, options, correct
#
# # Create text clip
# def make_text_clip(txt, fontsize=70, duration=2, pos='center'):
#     return TextClip(text=txt, font_size=fontsize, color='white', font="D:\\aaaa\\git\\Miniatures\\arial-bold.otf", method='caption', size=(720, None)).with_position(pos).with_duration(duration)
#
# # Create the video
# def render_quiz_video(output_path="quiz_video.mp4"):
#     W, H = 720, 1280  # TikTok vertical video size
#     bg_color = (10, 10, 30)
#
#     # Get quiz data
#     question, options, correct = generate_quiz()
#
#     # Background
#     bg = ColorClip(size=(W, H), color=bg_color, duration=10)
#
#     # On-screen text clips
#     intro = make_text_clip("🚨 Only 5% get this right...", duration=2, pos='center')
#     q_clip = make_text_clip(question, fontsize=60, duration=3)
#
#     options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
#     options_clip = make_text_clip(options_text, fontsize=60, duration=3)
#
#     answer_clip = make_text_clip(f"✅ Answer: {correct}", fontsize=65, duration=2)
#     outro_clip = make_text_clip("🧠 Boost your brain → link in bio", fontsize=55, duration=2)
#
#     # Combine into final video
#     final = CompositeVideoClip([
#         bg,
#         intro.with_start(0),
#         q_clip.with_start(2),
#         options_clip.with_start(5),
#         answer_clip.with_start(8),
#         outro_clip.with_start(10)
#     ], size=(W, H))
#
#     final.write_videofile(output_path, fps=24)
#
# # Run it
# if __name__ == "__main__":
#     render_quiz_video()

#todo reaarragne the text
#sync voice
#add the timer and the bell ring
#add the affiliate link description https://accounts.clickbank.com/master/login.html https://forgeniuswave.com/?hopId=54185358-b712-4989-bd77-65aae4106911
#add the tiktok api post
#add scheduler




def generate_quiz():
    question = "What comes next?\n2, 4, 8, 16, ___"
    options = ["18", "32", "24", "20"]
    correct = "32"
    return question, options, correct


def make_options_clips(options, correct_index, start_time=2, reveal_delay=3):
    clips = []
    for i, option in enumerate(options):
        # Initial clip (white color)
        base_clip = (TextClip(text= option, font_size=60, color='white', font='D:\\aaaa\\git\\Miniatures\\arial-bold.otf')
                     .with_position(("center", 200 + i * 80))
                     .with_start(start_time)
                     .with_duration(reveal_delay))
        clips.append(base_clip)

        # Highlighted clip (yellow), appears after delay
        if i == correct_index:
            highlight_clip = (TextClip(text=option, font_size=60, color='yellow', font='D:\\aaaa\\git\\Miniatures\\arial-bold.otf')
                              .with_position(("center", 200 + i * 80))
                              .with_start(start_time + reveal_delay)
                              .with_duration(2))  # Show for 2 seconds
            clips.append(highlight_clip)

    return clips


def make_text(txt, fontsize=60, y_pos=0.2, start_time=0, duration=8):
    y_pixel = int(1280 * y_pos)  # convert fractional y_pos to pixels

    return (TextClip(text =txt, font_size=fontsize, color='white', font="D:\\aaaa\\git\\Miniatures\\arial-bold.otf", method='caption', size=(680, None))
            .with_position(("center", y_pixel))
            .with_start(start_time)
            .with_duration(duration))

def generate_voice(text, filename="voice.mp3", speed_factor=1.3):
    # Generate TTS audio
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(filename)

    # Load audio and speed it up
    audio = AudioFileClip(filename)
    faster_audio = audio.with_speed_scaled(factor=speed_factor)
    output_path = "fast_" + filename
    faster_audio.write_audiofile(output_path)
    return "fast_" + filename

def make_timer_clip(start_time=0, countdown_from=5, duration=6):
    clips = []
    for i in range(countdown_from, -1, -1):
        timer_text = TextClip(text =f"{i}", font_size=80, color='yellow', font="D:\\aaaa\\git\\Miniatures\\arial-bold.otf")
        timer_text = (timer_text
                      .with_position(("center", 50))  # Top center
                      .with_start(start_time + (countdown_from - i))
                      .with_duration(1))
        clips.append(timer_text)
    return clips


def render_quiz_video(output_path="quiz_overlayed.mp4"):
    W, H = 720, 1280
    duration = 10
    bg = ColorClip(size=(W, H), color=(10, 10, 30), duration=duration)

    # Quiz content
    question, options, correct = generate_quiz()

    options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])

    # Text clips (appear at different times, on same screen)
    q_clip = make_text(question, fontsize=65, y_pos=0.15, start_time=0, duration=duration)
    #options_clip = make_text(options_text, fontsize=60, y_pos=0.4, start_time=2, duration=duration-2)
    correct_index=2
    options_clips = make_options_clips(options, correct_index, start_time=2, reveal_delay=3)

    answer_clip = make_text(f"✅ Answer: {correct}", fontsize=60, y_pos=0.75, start_time=4, duration=duration-4)
    cta_clip = make_text("🧠 Boost your brain → link in bio", fontsize=50, y_pos=0.9, start_time=6, duration=duration-6)


    # Voiceover
    voice_file = generate_voice(question, speed_factor=1.3)
    audio = AudioFileClip(voice_file)

    timer_clips = make_timer_clip(start_time=0, countdown_from=5, duration=6)

    # Final video
    #final = CompositeVideoClip([bg, q_clip, options_clip, answer_clip, cta_clip]+ timer_clips, size=(W, H))
    final = CompositeVideoClip([bg, q_clip]+ options_clips+[ answer_clip, cta_clip] + timer_clips, size=(W, H))
    final = final.with_audio(audio)

    final.write_videofile(output_path, fps=24)



if __name__ == "__main__":
    render_quiz_video()
