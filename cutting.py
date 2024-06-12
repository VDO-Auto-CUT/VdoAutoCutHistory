from moviepy.editor import VideoFileClip, concatenate_videoclips

def cut_video(input_video, output_video, start_time, end_time):
    video_clip = VideoFileClip(input_video)
    
    
    cut_clip = concatenate_videoclips([video_clip.subclip(0, start_time),
                                       video_clip.subclip(end_time, None)])
    
    cut_clip.write_videofile(output_video, codec='libx264', fps=60)  

    video_clip.close()

input_video = './vdo/pleng.mp4'
output_video = './vdo/plengcut.mp4'  
start_time = 0.001
end_time = 28.251

cut_video(input_video, output_video, start_time, end_time)