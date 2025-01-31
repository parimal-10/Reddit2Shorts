from moviepy import * # type: ignore
import getRedditPosts, getScreenshot, getConfig, time, subprocess, random, sys, math 
from os import listdir
from os.path import isfile, join

def createVideo():
    try:
        script = getRedditPosts.get_content()
    except:
        print("Error getting the videoscript")
        return None
    
    if(script == None):
        return None
    
    id = script.get_script_id()

    try:
        getScreenshot.getPostScreenshots(id, script)
    except:
        print("Error getting the screenshots")
        return None

    bgVideo = getConfig.get_bgvideo_filename()

    try:
        backgroundVideo = VideoFileClip(
            filename=bgVideo, 
            audio=False).subclipped(0, script.get_duration())
    except:
        print("Error creating the background video")
        return None
    
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

    final = CompositeVideoClip(
        clips=[backgroundVideo, contentOverlay], 
        size=backgroundVideo.size).with_audio(contentOverlay.audio)
    final.duration = script.get_duration()
    final.with_fps(backgroundVideo.fps)

    print("Rendering final video...")
    bitrate, threads = getConfig.get_video_config()
    outputFile = f"{getConfig.get_generated_video_directory()}/{id}.mp4"
    final.write_videofile(
        outputFile, 
        codec = 'mpeg4',
        threads = threads, 
        bitrate = bitrate
    )

    saveFile = getConfig.get_ids_storage_file()

    getRedditPosts.save_post_ids(id, saveFile)

    return id
