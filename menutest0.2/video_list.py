import os
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
import requests
from pytube import YouTube
import config
from functools import partial


class LinkListScreen(Screen):
    list_loaded = False

    def load_video_list(self):
        if self.list_loaded:
            pass
        else:
            for child_outer in self.children:
                if isinstance(child_outer, ScrollView):
                    for child in child_outer.children:
                        if isinstance(child, VideoButtons):
                            i = 0
                            for video in config.video_dict.keys():
                                b = Button(text=video, size_hint=(1, None), height=dp(150))
                                # Can modify the above to make GUI better. Do not modify: text, or on_press
                                # To modify size ask Csaba first
                                b.on_press = partial(child.video_button_press, video)
                                child.add_widget(b)
                                i += 1
                            if i == 0:
                                self.list_loaded = False
                            else:
                                self.list_loaded = True
                        else:
                            pass
                else:
                    pass

    def back_to_menu_button_press(self):
        self.manager.current = 'menu'
        config.previous_screen = 'menu'


class VideoButtons(StackLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.bind(minimum_height=self.setter('height'))
        self.has_connection = True

    def video_button_press(self, video_title):
        self.check_video_exists()
        self.check_internet_connection()
        if self.has_connection:
            self.download_video(video_title)
            self.parent.parent.manager.current = 'video'
            config.previous_screen = 'video'
        else:
            pass

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
        yt = YouTube(config.video_dict[video_title])
        stream = yt.streams.filter(res='720p').first()
        stream.download(filename='test.mp4')


class VideoScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.removable = ''

    def load_video(self):
        self.ids.video.source = 'test.mp4'
        self.ids.back_button.disabled = False

    def on_back_to_videos_button_press(self):
        self.manager.current = 'links'
        config.previous_screen = 'links'
        self.removable = self.ids.video.source
        self.ids.video.source = ''
        self.ids.video.state = 'stop'
        self.delete_previous_video()
        self.ids.back_button.disabled = True

    def delete_previous_video(self):
        if os.path.isfile(self.removable):
            os.remove(self.removable)
        else:
            pass
