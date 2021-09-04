import os
import certifi
import requests
import mysql.connector
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.stacklayout import StackLayout
from kivy.uix.videoplayer import VideoPlayer
from functools import partial
from pytube import YouTube

os.environ['SSL_CERT_FILE'] = certifi.where()

video_dict = {}
previous_screen = 'menu'


class ScreenManager1(ScreenManager):
    pass


class MenuScreen(Screen):
    has_connection = True

    def on_video_links_button_press(self):
        global video_dict
        if not video_dict:
            self.check_internet_connection()
            if self.has_connection:
                self.load_video_dict()
                self.manager.current = 'links'
                global previous_screen
                previous_screen = 'links'
            else:
                pass
        else:
            self.manager.current = 'links'
            previous_screen = 'links'

    def check_internet_connection(self):
        try:
            request = requests.get('https://www.youtube.com/', timeout=5)
            self.has_connection = True
        except (requests.ConnectionError, requests.Timeout) as exception:
            self.has_connection = False
            self.manager.current = 'net'

    def load_video_dict(self):
        global video_dict

        mydb = mysql.connector.connect(host='sql11.freemysqlhosting.net', user='sql11434313', passwd='IPt9fRRDYS', database='sql11434313')
        mycursor = mydb.cursor()
        mycursor.execute("Select links, titles from Videos")
        myresult = mycursor.fetchall()

        for row in myresult:
            video_dict[row[1]] = row[0]
            print("Link loaded")

class LinkListScreen(Screen):

    def back_to_menu_button_press(self):
        self.manager.current = 'menu'
        global previous_screen
        previous_screen = 'menu'


class VideoButtons(StackLayout):
    global video_dict
    has_connection = True
    list_loaded = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.bind(minimum_height=self.setter('height'))

        b = Button(text='Refresh List', size_hint=(1, None), height=dp(150))
        b.on_press = self.load_video_list
        self.add_widget(b)

    def load_video_list(self):
        global video_dict
        if self.list_loaded:
            pass
        else:
            i = 0
            for video in video_dict.keys():
                b = Button(text=video, size_hint=(1, None), height=dp(150))
                b.on_press = partial(self.video_button_press, video)
                self.add_widget(b)
                i += 1
            if i == 0:
                self.list_loaded = False
            else:
                self.list_loaded = True

    def video_button_press(self, video_title):
        self.check_video_exists()
        self.check_internet_connection()
        if self.has_connection:
            self.download_video(video_title)
            self.parent.parent.manager.current = 'video'
            global previous_screen
            previous_screen = 'video'

    def check_video_exists(self):
        if os.path.isfile('test.mp4'):
            os.remove('test.mp4')
        else:
            pass

    def check_internet_connection(self):
        try:
            request = requests.get('https://www.youtube.com/', timeout=5)
            self.has_connection = True
        except (requests.ConnectionError, requests.Timeout) as exception:
            self.has_connection = False
            self.parent.parent.manager.current = 'net'

    def download_video(self, video_title):
        yt = YouTube(video_dict[video_title])
        stream = yt.streams.filter(res='360p').first()
        stream.download(filename='test.mp4')
        print("Video Downloaded")


class NoNetScreen(Screen):

    def change_screen_back(self):
        global previous_screen
        self.manager.current = previous_screen


class VideoScreen(Screen):
    my_source = StringProperty('')
    removable = ''
    video_loaded = BooleanProperty(False)

    def on_load_video_press(self):
        self.my_source = 'test.mp4'
        self.video_loaded = True

    def on_back_to_videos_button_press(self):
        self.manager.current = 'links'
        global previous_screen
        previous_screen = 'links'
        self.removable = self.my_source
        self.my_source = ''
        self.delete_previous_video()
        self.video_loaded = False

    def delete_previous_video(self):
        if os.path.isfile(self.removable):
            os.remove(self.removable)
        else:
            pass


class MenuTestApp(App):
    pass


MenuTestApp().run()
