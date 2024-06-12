from moviepy.editor import *

# Load the mp4 file
video = VideoFileClip("./vdo/pleng.mp4")

# Extract audio from video
video.audio.write_audiofile("./vdo/pleng.mp3")