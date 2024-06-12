from moviepy.editor import *
video = VideoFileClip("./vod/pleng.mp4")
video.audio.write_audiofile("./vdo/converted_pleng.mp3")


from pydub import AudioSegment
audio = AudioSegment.from_mp3("./vdo/converted_pleng.mp3")

threshold = -40
silent_ranges = []
start_time = 0
silent_duration = 0

for i in range(len(audio)):
    if audio[i].dBFS < threshold:
        if start_time == 0:
            start_time = i / 1000
        silent_duration += 1
    else:
        if start_time != 0 and silent_duration >= 1000:  
            end_time = i / 1000 
            silent_ranges.append((start_time, end_time))
        start_time = 0
        silent_duration = 0

from moviepy.editor import VideoFileClip, concatenate_videoclips

def cut_video(input_video, output_video, silent_ranges):
    try:
        video_clip = VideoFileClip(input_video)
        duration = video_clip.duration
        subclips = []

        if silent_ranges[0][0] != 0:
            subclips.append(video_clip.subclip(0, silent_ranges[0][0]))

        for i in range(len(silent_ranges) - 1):
            subclips.append(video_clip.subclip(silent_ranges[i][1], silent_ranges[i+1][0]))

        if silent_ranges[-1][1] != duration:
            subclips.append(video_clip.subclip(silent_ranges[-1][1], duration))

        cut_clip = concatenate_videoclips(subclips)
        cut_clip.write_videofile(output_video, codec='libx264', fps=video_clip.fps)

        video_clip.close()
        cut_clip.close()

        os.remove('./vdo/converted_pleng.mp3')

        print("Video cut successfully.")
    except Exception as e:
        print("Error occurred:", e)
input = './vdo/pleng.mp4'
output_video = './vdo/pleng_cut.mp4'

cut_video(input, output_video, silent_ranges)