import os
import certifi
import requests
import mysql.connector
import random
import pickle
from kivy.app import App
from kivy.core.window import Window
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
    workouts_loaded = False
    load_able_workouts = []

    def load_workouts(self):
        global workout_ids
        global workouts
        global workout_buttons

        if not self.workouts_loaded:
            self.workouts_loaded = True
            self.load_able_workouts = []
            if os.path.isfile("save.dat"):
                with open("save.dat", "rb") as file:
                    self.load_able_workouts = pickle.load(file)
                    workout_ids = pickle.load(file)

                for workout_d in self.load_able_workouts:
                    w = WorkoutTemplate(name=str(workout_d["workout_index"]))
                    self.manager.add_widget(w)
                    w.selected_types = workout_d["selected_types"]
                    w.workout_index = workout_d["workout_index"]
                    w.workouts_length_on_create = workout_d["workouts_length_on_create"]
                    w.screen_name = workout_d["screen_name"]
                    w.label_text = workout_d["label_text"]
                    w.start_time = workout_d["start_time"]
                    w.end_time = workout_d["end_time"]
                    w.time_difference = workout_d["time_difference"]
                    w.workout_day = workout_d["workout_day"]
                    w.workout_name = workout_d["workout_name"]
                    w.workout_id = workout_d["workout_id"]
                    w.ids.start_time_spinner.text = workout_d["ids.start_time_spinner.text"]
                    w.ids.end_time_spinner.text = workout_d["ids.end_time_spinner.text"]
                    w.ids.workout_day_text.text = workout_d["ids.workout_day_text.text"]
                    w.ids.workout_name_input.text = workout_d["ids.workout_name_input.text"]
                    w.ids.custom_desc.text = workout_d["ids.custom_desc.text"]
                    w.ids.workout_types_selected.text = workout_d["ids.workout_types_selected.text"]
                    w.ids.delete_button.disabled = False
                    workouts.append(w)

                for worko in workouts:
                    b = Button(text=worko.workout_name, font_size=25, size_hint=(1 / 7, (0.8 / 24) * worko.time_difference),
                               pos_hint={"right": 1 / 7 * worko.workout_day, "top": (1 - (.8 / 24) * (worko.start_time-1))})
                    b.on_press = worko.on_workout_button_click
                    workout_buttons.append(b)
        else:
            pass

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

        def on_delete_all_button_press(self):
            global workouts
            global workout_buttons
            len_workouts = len(workouts)
            workout_buttons = []
            workouts = []
            for i in range(0, len_workouts):
                self.parent.add_buttons()

            if os.path.isfile("save.dat"):
                os.remove("save.dat")

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
                self.manager.remove_widget(child)
                del child

        for button in workout_buttons:
            if not button.parent == self:
                self.add_widget(button)


class WorkoutTemplate(Screen):
    days_dict = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5,
                 'Saturday': 6, 'Sunday': 7}

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
        self.ids.start_time_spinner.text = 'Starting time(by hour)'
        self.ids.end_time_spinner.text = 'End time(by hour)'
        self.workout_day = 0
        self.ids.workout_day_text.text = 'Select Day'
        self.workout_name = 'My workout'
        self.ids.workout_name_input.text = self.workout_name
        self.ids.custom_desc.text = 'Customisable workout description.'
        self.workout_id = 0
        self.ids.workout_types_selected.text = 'Selected Workout types: '

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
            self.workout_name = self.ids.workout_name_input.text
            while True:
                if self.workout_id == 0:
                    temp = random.randint(1, 200)
                    if temp not in workout_ids:
                        workout_ids.add(temp)
                        self.workout_id = temp
                        break

        if self.workouts_length_on_create > len(workouts):
            diff = self.workouts_length_on_create - len(workouts)
            self.workout_index -= diff

        if self.time_difference == 99:
            self.time_difference = t_diff
            button = Button(text=self.workout_name, font_size=25, size_hint=(1/7, (0.8/24)*self.time_difference),
                            pos_hint={"right": 1/7*self.workout_day, "top": (1-(.8/24)*(self.start_time-1))})
            button.on_press = self.on_workout_button_click
            workout_buttons.append(button)
        else:
            self.time_difference = t_diff
            self.workout_name = self.ids.workout_name_input.text
            workout_buttons[self.workout_index].text = self.workout_name
            workout_buttons[self.workout_index].size_hint = (1/7, (0.8/24)*self.time_difference)
            workout_buttons[self.workout_index].pos_hint = {"right": 1/7*self.workout_day,
                                                            "top": (1-(.8/24)*(self.start_time-1))}

        self.ids.delete_button.disabled = False
        if os.path.isfile("save.dat"):
            os.remove("save.dat")
        save_workouts()
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

        if os.path.isfile("save.dat"):
            os.remove("save.dat")
        save_workouts()

        self.manager.current = 'editor'
        previous_screen = 'editor'

    def on_back_without_saving_button_press(self):
        global previous_screen

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
            text_len = len(self.label_text)
            for i in range(text_len, text_len-(len(removable)+2), -1):
                length = len(self.label_text)
                self.label_text = self.label_text[:length-1]
            self.ids.workout_types_selected.text = self.label_text

    def starting_time_selected(self, value):
        worked = True
        try:
            int(value)
        except:
            worked = False

        if worked:
            self.ids.end_time_spinner.text = 'End time(by hour)'
            self.ids.save_button.disabled = True
            self.start_time = int(value)
            end_time_values = []
            for i in range(self.start_time+1, 25):
                end_time_values.append(str(i))
            self.ids.end_time_spinner.values = end_time_values
            self.ids.end_time_spinner.disabled = False
        else:
            pass

    def end_time_selected(self, value):
        if not value == 'End time(by hour)':
            self.end_time = int(value)
            if not self.workout_day == 0:
                self.ids.save_button.disabled = False
        else:
            pass

    def day_selected(self, value):
        if not value == 'Select Day':
            self.workout_day = self.days_dict[value]
            if not self.ids.end_time_spinner.text == 'End time(by hour)':
                self.ids.save_button.disabled = False
        else:
            pass


def save_workouts():
    global workout_ids

    save_able_workouts = []

    for workout in workouts:
        workout_dict = {"selected_types": workout.selected_types, "workout_index": workout.workout_index,
                        "workouts_length_on_create": workout.workouts_length_on_create,
                        "screen_name": workout.screen_name, "label_text": workout.label_text,
                        "start_time": workout.start_time, "end_time": workout.end_time,
                        "time_difference": workout.time_difference, "workout_day": workout.workout_day,
                        "workout_name": workout.workout_name, "workout_id": workout.workout_id,
                        "ids.start_time_spinner.text": workout.ids.start_time_spinner.text,
                        "ids.end_time_spinner.text": workout.ids.end_time_spinner.text,
                        "ids.workout_day_text.text": workout.ids.workout_day_text.text,
                        "ids.workout_name_input.text": workout.ids.workout_name_input.text,
                        "ids.custom_desc.text": workout.ids.custom_desc.text,
                        "ids.workout_types_selected.text": workout.ids.workout_types_selected.text}
        save_able_workouts.append(workout_dict)

    with open("save.dat", "wb") as f:
        pickle.dump(save_able_workouts, f)
        pickle.dump(workout_ids, f)


class MenuTestApp(App):
    # def __init__(self, **kwargs):
        # super().__init__(**kwargs)
        # Window.size = (540, 1200)
    pass


MenuTestApp().run()
