import os
from user import User
import threading
from pytube import YouTube
previous_screen = 'menu'  # needed for no_net_screen and bad_input_screen change
user = User()  # creating user for storing user data
video_dict = {}  # dictionary of video names(keys) and links(values)
workouts = []  # list of workout_templates
workout_buttons = []  # list of buttons bind to workout_templates
workout_ids = set(())  # set of workout_templates screen names
host = 'sql11.freemysqlhosting.net'  # database server IP
database_user = 'sql11434313'  # database username
passwd = 'IPt9fRRDYS'  # database password
database = 'sql11434313'  # database name
app_color = ""
current_thread = ()
current_thread_id = 0
thread_ids = []


def download_video(video_title, thread_id):
    global current_thread_id
    yt = YouTube(video_dict[video_title])
    stream = yt.streams.filter(res='720p').first()
    downloadable_filename = str(thread_id) + ".mp4"
    stream.download(filename=downloadable_filename)
    if thread_id not in thread_ids:
        os.remove(downloadable_filename)
    else:
        os.rename(downloadable_filename, 'test.mp4')
        thread_ids.remove(thread_id)


def create_thread(video_title, thread_id):
    global current_thread
    download_thread = threading.Thread(target=download_video, args=(video_title, thread_id,), daemon=True)
    current_thread = download_thread
