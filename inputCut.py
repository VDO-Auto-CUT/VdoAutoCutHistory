from tkinter import filedialog
from tkinter import *
from moviepy.editor import *
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def select_video():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4")])
    return file_path

# Select video file using file explorer
input_video = select_video()

# Convert video to audio
video = VideoFileClip(input_video)
video.audio.write_audiofile("ml_audio1.mp3")

# Load the MP3 file
audio = AudioSegment.from_mp3("ml_audio1.mp3")

# Define the threshold for silence detection (in dBFS)
threshold = -30

# Find silent parts
silent_ranges = []

# Initialize start time
start_time = 0

# Minimum duration for a silent part to be considered for cutting (in seconds)
min_silent_duration = 1

# Loop through the audio
for i in range(len(audio)):
    # Check if the audio frame's dBFS is below the threshold
    if audio[i].dBFS < threshold:
        # If the previous frame was not silent, set the start time
        if start_time == 0:
            start_time = i / 1000  # Convert milliseconds to seconds
    else:
        # If the previous frame was silent, check the duration
        if start_time != 0:
            end_time = i / 1000  # Convert milliseconds to seconds
            silent_duration = end_time - start_time
            if silent_duration >= min_silent_duration:
                silent_ranges.append((start_time, end_time))
            start_time = 0  # Reset start time

def cut_video(input_video, output_video, silent_ranges):
    try:
        video_clip = VideoFileClip(input_video)
        duration = video_clip.duration
        subclips = []

        # Add the first subclip if the first silent range doesn't start at time 0
        if silent_ranges[0][0] != 0:
            subclips.append(video_clip.subclip(0, silent_ranges[0][0]))

        # Add subclips between silent ranges
        for i in range(len(silent_ranges) - 1):
            subclips.append(video_clip.subclip(silent_ranges[i][1], silent_ranges[i+1][0]))

        # Add the last subclip if the last silent range doesn't end at the video's duration
        if silent_ranges[-1][1] != duration:
            subclips.append(video_clip.subclip(silent_ranges[-1][1], duration))

        # Concatenate the subclips
        cut_clip = concatenate_videoclips(subclips)

        # Write the concatenated clip to the output video file
        cut_clip.write_videofile(output_video, codec='libx264', fps=video_clip.fps)

        # Close the video clip objects
        video_clip.close()
        cut_clip.close()

        print("Video cut successfully.")
    except Exception as e:
        print("Error occurred:", e)

output_video = 'final_cut.mp4'

cut_video(input_video, output_video, silent_ranges)

# Remove the MP3 file
os.remove("ml_audio1.mp3")
