from moviepy.editor import VideoFileClip, concatenate_videoclips

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

input_video = './vdo/pleng.mp4'
output_video = './vdo/plengafterCut.mp4'
silent_ranges = [(0.001, 28.251), (61.158, 77.064)]

cut_video(input_video, output_video, silent_ranges)