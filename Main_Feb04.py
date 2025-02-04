from tkinter import filedialog
from tkinter import *
from moviepy.editor import VideoFileClip, concatenate_videoclips, concatenate_audioclips, AudioFileClip
from pydub import AudioSegment
from pydub.effects import normalize
import os   
import noisereduce as nr
import numpy as np
import assemblyai as aai
import subprocess

# Set up AssemblyAI API key
aai.settings.api_key = "359db971808244f994b25882ec6e285d"

def select_video():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
    return file_path

def enhance_sound(audio_path):
    try:
        # Load the audio file
        audio = AudioSegment.from_file(audio_path)

        # Convert audio to numpy array
        samples = np.array(audio.get_array_of_samples())
        
        # Perform noise reduction
        reduced_noise = nr.reduce_noise(y=samples, sr=audio.frame_rate)
        
        # Convert reduced noise signal back to audio (make sure to reshape for stereo if needed)
        reduced_audio = AudioSegment(
            reduced_noise.tobytes(), 
            frame_rate=audio.frame_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )

        # Normalize the audio
        normalized_audio = normalize(reduced_audio)

        # Export the enhanced audio
        enhanced_audio_path = "enhanced_audio.mp3"
        normalized_audio.export(enhanced_audio_path, format="mp3")

        return enhanced_audio_path
    except Exception as e:
        print("Error enhancing audio:", e)
        return None
def convert_video_to_audio(input_video):
    video = VideoFileClip(input_video)
    video.audio.write_audiofile("ml_audio1.mp3")

def load_audio():
    return AudioSegment.from_file("enhanced_audio.mp3", format="mp3")

def find_silent_ranges(audio, threshold=-40, min_silent_duration=1):
    silent_ranges = []
    start_time = 0

    for i in range(len(audio)):
        if audio[i].dBFS < threshold:
            if start_time == 0:
                start_time = i / 1000
        else:
            if start_time != 0:
                end_time = i / 1000
                silent_duration = end_time - start_time
                if silent_duration >= min_silent_duration:
                    silent_ranges.append((start_time, end_time))
                start_time = 0

    return silent_ranges

def cut_video(input_video, output_video, silent_ranges):
    try:
        video_clip = VideoFileClip(input_video)
        audio_clip = video_clip.audio
        duration = video_clip.duration
        subclips = []
        audio_subclips = []

        if silent_ranges[0][0] != 0:
            subclips.append(video_clip.subclip(0, silent_ranges[0][0]))
            audio_subclips.append(audio_clip.subclip(0, silent_ranges[0][0]))

        for i in range(len(silent_ranges) - 1):
            subclips.append(video_clip.subclip(silent_ranges[i][1], silent_ranges[i+1][0]))
            audio_subclips.append(audio_clip.subclip(silent_ranges[i][1], silent_ranges[i+1][0]))

        if silent_ranges[-1][1] != duration:
            subclips.append(video_clip.subclip(silent_ranges[-1][1], duration))
            audio_subclips.append(audio_clip.subclip(silent_ranges[-1][1], duration))

        cut_clip = concatenate_videoclips(subclips)
        cut_audio = concatenate_audioclips(audio_subclips)

        cut_clip = cut_clip.set_audio(cut_audio)
        cut_clip.write_videofile(output_video, codec='libx264', fps=video_clip.fps, audio_codec='aac')

        video_clip.close()
        cut_clip.close()

        print("Video cut successfully.")
    except Exception as e:
        print("Error occurred:", e)

def transcribe_audio(audio_path):
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_path)

        # Save subtitles to an SRT file
        srt_file = "transcript.srt"
        with open(srt_file, "w") as file:
            file.write(transcript.export_subtitles_srt())

        print(f"Subtitle saved to {srt_file}")
        return srt_file
    except Exception as e:
        print("Error transcribing audio:", e)
        return None



def adjust_subtitles(srt_path, silent_ranges):
    try:
        with open(srt_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        current_time_offset = 0
        silent_index = 0

        for line in lines:
            if "-->" in line:
                start_time, end_time = line.split(" --> ")
                start_time = convert_to_seconds(start_time)
                end_time = convert_to_seconds(end_time)

                while silent_index < len(silent_ranges) and start_time >= silent_ranges[silent_index][0]:
                    current_time_offset += silent_ranges[silent_index][1] - silent_ranges[silent_index][0]
                    silent_index += 1

                start_time -= current_time_offset
                end_time -= current_time_offset

                new_lines.append(f"{convert_to_timestamp(start_time)} --> {convert_to_timestamp(end_time)}\n")
            else:
                new_lines.append(line)

        new_srt_path = "adjusted_transcript.srt"
        with open(new_srt_path, "w") as file:
            file.writelines(new_lines)

        return new_srt_path
    except Exception as e:
        print("Error adjusting subtitles:", e)
        return None

def convert_to_seconds(timestamp):
    h, m, s = map(float, timestamp.replace(",", ".").split(":"))
    return h * 3600 + m * 60 + s

def convert_to_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:06.3f}".replace(".", ",")

def embed_subtitles(video_path, srt_path, output_path):
    try:
        if not os.path.exists(video_path):
            print(f"Error: {video_path} does not exist.")
            return

        command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"subtitles='{srt_path}'",
            output_path
        ]
        subprocess.run(command, check=True)
        print(f"Subtitles embedded successfully into {output_path}")
    except subprocess.CalledProcessError as e:
        print("Error embedding subtitles:", e)

def main():
    input_video = select_video()
    if not input_video:
        print("No video file selected.")
        return
    convert_video_to_audio(input_video)
    enhanced_audio_path = enhance_sound("ml_audio1.mp3")
    if enhanced_audio_path:
        print("Audio enhanced successfully.")
    audio = load_audio()
    silent_ranges = find_silent_ranges(audio)
    os.remove("ml_audio1.mp3")
    
    if silent_ranges:
        cut_video_path = 'cut_video.mp4'
        cut_video(input_video, cut_video_path, silent_ranges)
        if os.path.exists(cut_video_path):
            print(f"{cut_video_path} created successfully.")
        else:
            print(f"Error: {cut_video_path} was not created.")
            return
        srt_file = transcribe_audio(enhanced_audio_path)
        if srt_file:
            adjusted_srt_file = adjust_subtitles(srt_file, silent_ranges)
            output_video_with_subs = 'final_video_with_subs.mp4'
            embed_subtitles(cut_video_path, adjusted_srt_file, output_video_with_subs)
        os.remove(enhanced_audio_path)
    else:
        print("No silent parts found in the audio.")
    
    os.remove("adjusted_transcript.srt")
    # os.remove("transcript.srt")
    os.remove("cut_video.mp4")

if __name__ == "__main__":
    main()
