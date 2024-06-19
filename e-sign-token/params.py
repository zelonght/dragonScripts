import os

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
APPS_TO_CHECK = ["ecussign_pro.exe", "chrome.exe", "msedge.exe"]
SLEEPING = 20
FFMEG_CMD = "ffmpeg -f gdigrab -framerate 15 -video_size 1280x720 -i desktop {}"
record_started = None
record_max_hours = 1 * 60 * 60 # Slit sessions every 1 hour 
ffmeg_p = None