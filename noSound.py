from pydub import AudioSegment

# Load the MP3 file
audio = AudioSegment.from_mp3("./vdo/pleng.mp3")

# Define the threshold for silence detection (in dBFS)
threshold = -40

# Find silent parts
silent_ranges = []

# Initialize start time
start_time = 0

# Initialize a variable to track the duration of the silent period
silent_duration = 0

# Loop through the audio
for i in range(len(audio)):
    # Check if the audio frame's dBFS is below the threshold
    if audio[i].dBFS < threshold:
        # If the previous frame was not silent, set the start time
        if start_time == 0:
            start_time = i / 1000  # Convert milliseconds to seconds
        # Increment the silent duration
        silent_duration += 1
    else:
        # If the previous frame was silent and the silent duration is at least 5 seconds
        if start_time != 0 and silent_duration >= 5000:  # 5000 milliseconds = 5 seconds
            end_time = i / 1000  # Convert milliseconds to seconds
            silent_ranges.append((start_time, end_time))
        # Reset start time and silent duration
        start_time = 0
        silent_duration = 0

# Output the list of silent ranges as a list of tuples (start_time, end_time)
print("Silent Moments (5 seconds or longer):")
print(silent_ranges)
