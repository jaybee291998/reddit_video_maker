from moviepy.editor import *

clip = VideoFileClip("../test_vid.mp4").subclip(50, 54)

image_clip1 = ImageClip("../ss1.png", duration=2)

image_clip2 = ImageClip("../ss2.png", duration=2)



# image_clip1 = image_clip1.set_position(center_position)
# image_clip2 = image_clip2.set_position(center_position)

image_clips = concatenate_videoclips([image_clip1, image_clip2])
# Get the center position for the image clip
center_position = (clip.size[0] // 2 - image_clips.size[0] // 2, clip.size[1] // 2 - image_clips.size[1] // 2)
image_clips = image_clips.set_position(center_position)
video = CompositeVideoClip(clips=[clip, image_clips])
video.write_videofile("../test_vid_edited.mp4", fps=24)