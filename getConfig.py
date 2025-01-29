import os
import sys

def get_current_directory():
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def get_ids_storage_file():
    return get_current_directory() + "/videos.json"

def get_voice_over_directory():
    return get_current_directory() + "/voiceover"

def get_screenshot_directory():
    return get_current_directory() + "/screenshot"

def get_screen_config():
    return 400, 800

def get_bgvideo_filename():
    return get_current_directory() + "/vid.mp4"

def get_margin_size():
    return 64

def get_video_config():
    return "8000k", 12

def get_initial_post_count():
    return 10