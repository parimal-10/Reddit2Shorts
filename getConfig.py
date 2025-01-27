import os
import sys

def get_current_directory():
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def get_ids_storage_file():
    return get_current_directory() + "/videos.json"

def get_voice_over_directory():
    return get_current_directory() + "/voiceover"
