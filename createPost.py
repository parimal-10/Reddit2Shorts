from moviepy import * # type: ignore
import getRedditPosts, getScreenshot, getConfig, time, subprocess, random, sys, math 
from os import listdir
from os.path import isfile, join

def createVideo():
    script = getRedditPosts.get_content()
    
    if(script == None):
        return createVideo()
    print("get_content() executed")
    id = script.get_script_id()

    getScreenshot.getPostScreenshots(id, script)

    bgVideo = getConfig.get_bgvideo_filename()

    backgroundVideo = VideoFileClip(
        filename=bgVideo, 
        audio=False).subclipped(0, script.get_duration())
    
    w, h = backgroundVideo.size

    def __create_clip(screenshotFile, audioClip, marginSize):
        imageClip = ImageClip(
            screenshotFile,
            duration = audioClip.duration
        ).with_position(("center", "center"))
        imageClip = imageClip.resized(width=(w-marginSize))
        videoClip = imageClip.with_audio(audioClip)
        videoClip.fps = 1
        return videoClip

    clips = []
    marginSize = getConfig.get_margin_size()
    clips.append(__create_clip(script.titleSCFile, script.titleAudioClip, marginSize))
    clips.append(__create_clip(script.textSCFile, script.textAudioClip, marginSize))
    for comment in script.frames:
        print("comment clip addidtion done")
        clips.append(__create_clip(comment.screenShotFile, comment.audioClip, marginSize))

    contentOverlay = concatenate_videoclips(clips).with_position(("center", "center"))

    # Compose background/foreground
    final = CompositeVideoClip(
        clips=[backgroundVideo, contentOverlay], 
        size=backgroundVideo.size).with_audio(contentOverlay.audio)
    final.duration = script.get_duration()
    final.with_fps(backgroundVideo.fps)

    # Write output to file
    print("Rendering final video...")
    bitrate, threads = getConfig.get_video_config()
    outputFile = f"{getConfig.get_generated_video_directory()}/{id}.mp4"
    final.write_videofile(
        outputFile, 
        codec = 'mpeg4',
        threads = threads, 
        bitrate = bitrate
    )


if __name__ == "__main__":
    createVideo()
