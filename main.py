import os
import certifi
import requests
import mysql.connector
import random
from kivy.app import App
from kivy.graphics import Color, Line
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.spinner import Spinner
from kivy.uix.stacklayout import StackLayout
from kivy.uix.videoplayer import VideoPlayer
from functools import partial

from kivy.uix.widget import Widget
from pytube import YouTube

os.environ['SSL_CERT_FILE'] = certifi.where()

video_dict = {}
previous_screen = 'menu'
workouts = []
workout_buttons = []
workout_ids = set(())


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

    def on_workout_editor_button_press(self):
        global previous_screen
        self.manager.current = 'editor'
        previous_screen = 'editor'

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


class WorkoutEditor(Screen):

    class Display1(FloatLayout):
        vertical_lines = []
        horizontal_lines = []

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.init_vertical_lines()
            self.init_horizontal_lines()

        def on_size(self, *args):
            self.update_vertical_lines()
            self.update_horizontal_lines()

        def init_vertical_lines(self):
            with self.canvas.before:
                Color(1, 1, 1)
                for i in range(0, 8):
                    self.vertical_lines.append(Line())

        def update_vertical_lines(self):
            for i in range(0, 8):
                x1, y1 = 0+i/7*self.width, .2 * self.height
                x2, y2 = 0+i/7*self.width, self.height
                self.vertical_lines[i].points = [x1, y1, x2, y2]

        def init_horizontal_lines(self):
            with self.canvas.before:
                Color(1, 1, 1)
                for i in range(0, 25):
                    self.horizontal_lines.append(Line())

        def update_horizontal_lines(self):
            for i in range(0, 25):
                x1, y1 = 0, .2*self.height + i/30*self.height
                x2, y2 = self.width, .2*self.height + i/30*self.height
                self.horizontal_lines[i].points = [x1, y1, x2, y2]

        def on_back_button_press(self):
            global previous_screen
            self.parent.manager.current = 'menu'
            previous_screen = 'menu'

        def on_add_new_button_press(self):
            global previous_screen
            new_workout_screen = WorkoutTemplate(name='temp')
            self.parent.manager.add_widget(new_workout_screen)
            self.parent.manager.current = 'temp'
            previous_screen = 'temp'

    def add_buttons(self):
        global workout_buttons
        global workouts
        for child in self.children:
            if isinstance(child, Button) and child not in workout_buttons:
                self.remove_widget(child)
                del child
            else:
                pass

        for child in self.manager.children:
            if isinstance(child, WorkoutTemplate) and child not in workouts:
                self.remove_widget(child)
                del child

        for button in workout_buttons:
            if not button.parent == self:
                self.add_widget(button)


class WorkoutTemplate(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global workouts
        self.selected_types = []
        self.workout_index = len(workouts)
        self.workouts_length_on_create = len(workouts) + 1
        self.screen_name = ''
        self.label_text = 'Selected Workout types: '
        self.start_time = 99
        self.end_time = 99
        self.time_difference = 99
        self.workout_name = ''
        self.workout_id = 0

    def spinner_clicked(self, value):
        if value not in self.selected_types:
            self.selected_types.append(value)
            self.label_text += value+', '

        self.ids.workout_types_selected.text = self.label_text

    def on_save_workout_button_press(self):
        global workouts
        global workout_buttons
        global workout_ids
        global previous_screen
        t_diff = self.end_time - self.start_time
        if self not in workouts:
            workouts.append(self)
            self.workout_name = 'Workout ' + str(len(workouts))
            while True:
                if self.workout_id == 0:
                    temp = random.randint(1, 200)
                    if temp not in workout_ids:
                        workout_ids.add(temp)
                        self.workout_id = temp
                        break
        if self.time_difference == 99:
            self.time_difference = t_diff
            button = Button(text=self.workout_name, size_hint=(1/7, (0.8/24)*self.time_difference), pos_hint={"center_x": 1/7/2, "top":(1-(.8/24)*self.start_time)})
            button.on_press = self.on_workout_button_click
            workout_buttons.append(button)
        elif not t_diff == self.time_difference:
            self.time_difference = t_diff
            if self.workouts_length_on_create > len(workouts):
                diff = self.workouts_length_on_create - len(workouts)
                self.workout_index -= diff
            workout_buttons.pop(self.workout_index)
            button = Button(text=self.workout_name, size_hint=(1 / 7, (0.8 / 24) * self.time_difference),
                            pos_hint={"center_x": 1 / 7 / 2, "top": (1 - (.8 / 24) * self.start_time)})
            button.on_press = self.on_workout_button_click
            workout_buttons.insert(self.workout_index, button)

        self.manager.current = 'editor'
        previous_screen = 'editor'

    def on_delete_workout_button_press(self):
        global workout_buttons
        global workouts
        global previous_screen
        global workout_ids

        if self.workouts_length_on_create > len(workouts):
            diff = self.workouts_length_on_create - len(workouts)
            self.workout_index -= diff

        workouts.pop(self.workout_index)
        workout_buttons.pop(self.workout_index)
        workout_ids.remove(self.workout_id)

        self.manager.current = 'editor'
        previous_screen = 'editor'

    def on_temp_leave(self):
        global workouts
        if self.name == 'temp':
            self.name = str(self.workout_id)
        else:
            pass

    def on_workout_button_click(self):
        global previous_screen
        self.manager.current = self.name
        previous_screen = self.name

    def on_remove_last_button_press(self):
        if len(self.selected_types) > 0:
            removable = self.selected_types.pop()
            print(removable)
            text_len = len(self.label_text)
            for i in range(text_len, text_len-(len(removable)+2), -1):
                length = len(self.label_text)
                self.label_text = self.label_text[:length-1]
            self.ids.workout_types_selected.text = self.label_text

    def starting_time_selected(self, value):
        self.ids.end_time_spinner.text = 'End time(by hour)'
        self.ids.save_button.disabled = True
        self.start_time = int(value)
        end_time_values = []
        for i in range(self.start_time+1, 25):
            end_time_values.append(str(i))
        self.ids.end_time_spinner.values = end_time_values
        self.ids.end_time_spinner.disabled = False

    def end_time_selected(self, value):
        if not value == 'End time(by hour)':
            self.end_time = int(value)
            self.ids.save_button.disabled = False
        else:
            pass


class MenuTestApp(App):
    pass


MenuTestApp().run()
