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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
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


class User:
    def __init__(self):
        self.body_mass = 'Mass in kg'
        self.height = 'Height in cm'
        self.age = 'Age in years'
        self.sex = 'Male/Female'
        self.activity = 'Level of Activity'
        self.goal = 'Training Goal'
        self.macros = {"Calories": 0, "Carbs": 0, "Fats": 0, "Proteins": 0}
        self.macros_used = {"Calories": 0, "Carbs": 0, "Fats": 0, "Proteins": 0}
        load_user_data(self)


def save_user_data(user_object):
    with open("user.dat", "wb") as save:
        pickle.dump(user_object.body_mass, save)
        pickle.dump(user_object.height, save)
        pickle.dump(user_object.age, save)
        pickle.dump(user_object.sex, save)
        pickle.dump(user_object.activity, save)
        pickle.dump(user_object.goal, save)
        pickle.dump(user_object.macros, save)
        pickle.dump(user_object.macros_used, save)


def load_user_data(user_object):
    if os.path.isfile("user.dat"):
        with open("user.dat", "rb") as save:
            user_object.body_mass = pickle.load(save)
            user_object.height = pickle.load(save)
            user_object.age = pickle.load(save)
            user_object.sex = pickle.load(save)
            user_object.activity = pickle.load(save)
            user_object.goal = pickle.load(save)
            user_object.macros = pickle.load(save)
            user_object.macros_used = pickle.load(save)
    else:
        pass


user = User()


class ScreenManager1(ScreenManager):
    pass


class MenuScreen(Screen):
    has_connection = True
    workouts_loaded = False
    load_able_workouts = []
    calorie_displayed = ''
    carb_displayed = ''
    fat_displayed = ''
    protein_displayed = ''
    created = False

    def on_pre_enter(self, *args):
        self.calorie_displayed = str(user.macros_used["Calories"]) + "kcal/" + str(user.macros["Calories"]) + "kcal"
        self.carb_displayed = "Carbs: " + str(user.macros_used["Carbs"]) + "g/" + str(user.macros["Carbs"]) + "g"
        self.fat_displayed = "Fats: " + str(user.macros_used["Fats"]) + "g/" + str(user.macros["Fats"]) + "g"
        self.protein_displayed = "Proteins: " + str(user.macros_used["Proteins"]) + "g/" + str(user.macros["Proteins"]) + "g"
        if self.created:
            self.print_labels()
        else:
            self.created = True

    def print_labels(self):
        self.ids.calorie_label.text = str(user.macros_used["Calories"]) + "kcal/" + str(user.macros["Calories"]) + "kcal"
        self.ids.carb_label.text = "Carbs: " + str(user.macros_used["Carbs"]) + "g/" + str(user.macros["Carbs"]) + "g"
        self.ids.fat_label.text = "Fats: " + str(user.macros_used["Fats"]) + "g/" + str(user.macros["Fats"]) + "g"
        self.ids.protein_label.text = "Proteins: " + str(user.macros_used["Proteins"]) + "g/" + str(user.macros["Proteins"]) + "g"

        if user.macros_used["Calories"] > user.macros["Calories"]:
            self.ids.calorie_label.color = (1, 0, 0)
        else:
            self.ids.calorie_label.color = (1, 1, 1)
        if user.macros_used["Carbs"] > user.macros["Carbs"]:
            self.ids.carb_label.color = (1, 0, 0)
        else:
            self.ids.carb_label.color = (1, 1, 1)
        if user.macros_used["Fats"] > user.macros["Fats"]:
            self.ids.fat_label.color = (1, 0, 0)
        else:
            self.ids.fat_label.color = (1, 1, 1)
        if user.macros_used["Proteins"] > user.macros["Proteins"]:
            self.ids.protein_label.color = (1, 0, 0)
        else:
            self.ids.protein_label.color = (1, 1, 1)

    def on_plus_button_press(self, box):
        if box == self.ids.calorie:
            try:
                user.macros_used["Calories"] += float(self.ids.calorie_input.text)
                self.print_labels()
                save_user_data(user)
            except:
                self.manager.current = 'bad_input'
        elif box == self.ids.carb:
            try:
                user.macros_used["Carbs"] += float(self.ids.carb_input.text)
                self.print_labels()
                save_user_data(user)
            except:
                self.manager.current = 'bad_input'
        elif box == self.ids.fat:
            try:
                user.macros_used["Fats"] += float(self.ids.fat_input.text)
                self.print_labels()
                save_user_data(user)
            except:
                self.manager.current = 'bad_input'
        elif box == self.ids.protein:
            try:
                user.macros_used["Proteins"] += float(self.ids.protein_input.text)
                self.print_labels()
                save_user_data(user)
            except:
                self.manager.current = 'bad_input'
        else:
            pass

    def on_minus_button_press(self, box):
        if box == self.ids.calorie:
            try:
                if user.macros_used["Calories"] >= float(self.ids.calorie_input.text):
                    user.macros_used["Calories"] -= float(self.ids.calorie_input.text)
                    self.print_labels()
                    save_user_data(user)
                else:
                    self.ids.calorie_input.text = "Too big number"
            except:
                self.manager.current = 'bad_input'
        elif box == self.ids.carb:
            try:
                if user.macros_used["Carbs"] >= float(self.ids.carb_input.text):
                    user.macros_used["Carbs"] -= float(self.ids.carb_input.text)
                    self.print_labels()
                    save_user_data(user)
                else:
                    self.ids.carb_input.text = "Too big number"
            except:
                self.manager.current = 'bad_input'
        elif box == self.ids.fat:
            try:
                if user.macros_used["Fats"] >= float(self.ids.fat_input.text):
                    user.macros_used["Fats"] -= float(self.ids.fat_input.text)
                    self.print_labels()
                    save_user_data(user)
                else:
                    self.ids.fat_input.text = "Too big number"
            except:
                self.manager.current = 'bad_input'
        elif box == self.ids.protein:
            try:
                if user.macros_used["Proteins"] >= float(self.ids.protein_input.text):
                    user.macros_used["Proteins"] -= float(self.ids.protein_input.text)
                    self.print_labels()
                    save_user_data(user)
                else:
                    self.ids.protein_input.text = "Too big number"
            except:
                self.manager.current = 'bad_input'
        else:
            pass

    def on_reset_intake_button_press(self):
        user.macros_used = {"Calories": 0, "Carbs": 0, "Fats": 0, "Proteins": 0}
        self.print_labels()
        save_user_data(user)

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
                    w.ids.examples.text = "Examples"
                    w.examples_values = workout_d["examples_values"]
                    w.ids.examples.values = w.examples_values
                    w.examples_dict = workout_d["examples_dict"]
                    w.added_example_types = workout_d["added_example_types"]
                    w.ids.examples.disabled = False
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
            mydb = mysql.connector.connect(host='sql11.freemysqlhosting.net', user='sql11434313',
                                           passwd='IPt9fRRDYS', database='sql11434313')
            self.has_connection = True
        except:
            self.has_connection = False
            self.manager.current = 'net'

    def load_video_dict(self):
        global video_dict

        mydb = mysql.connector.connect(host='sql11.freemysqlhosting.net', user='sql11434313',
                                       passwd='IPt9fRRDYS', database='sql11434313')
        mycursor = mydb.cursor()
        mycursor.execute("Select links, titles from Videos")
        myresult = mycursor.fetchall()

        for row in myresult:
            video_dict[row[1]] = row[0]
            # print("Link loaded")

    def on_workout_editor_button_press(self):
        global previous_screen
        self.manager.current = 'editor'
        previous_screen = 'editor'

    def on_calorie_calculator_button_press(self):
        global previous_screen
        self.manager.current = 'input'
        previous_screen = 'input'


class UserDataScreen(Screen):
    activity_dict = {"Sedentary(little or no exercise, desk job)": 1.2,
                     "Lightly active(light exercise/ sports 1-3 days/week)": 1.375,
                     "Moderately active(moderate exercise/ sports 6-7 days/week)": 1.55,
                     "Very active(hard exercise every day, or exercising 2 xs/day)": 1.725,
                     "Extra active(hard exercise 2 or more times per day)": 1.9}
    goal_dict = {"Maintain mass": 1, "Mild mass loss": .9, "Mass loss": .79, "Extreme mass loss": .59,
                 "Mild mass gain": 1.1, "Mass gain": 1.21, "Fast mass gain": 1.41}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global user
        self.results = user.macros
        self.body_mass = user.body_mass
        self.height_attr = user.height
        self.age = user.age
        self.sex = user.sex
        self.activity = user.activity
        self.goal = user.goal

    def on_pre_enter(self, *args):
        self.ids.body_mass.text = user.body_mass
        self.ids.height.text = user.height
        self.ids.age.text = user.age
        self.ids.sex.text = user.sex
        self.ids.activity.text = user.activity
        self.ids.goal.text = user.goal
        self.print_results()

    def on_leave(self, *args):
        self.ids.results.text = ''

    def on_calculate_button_press(self):
        if self.check_all_inputs():
            self.body_mass = self.ids.body_mass.text
            self.height_attr = self.ids.height.text
            self.age = self.ids.age.text
            self.sex = self.ids.sex.text
            self.activity = self.ids.activity.text
            self.goal = self.ids.goal.text
            if self.ids.sex.text == 'Male':
                bmr = 66 + 13.7*float(self.ids.body_mass.text) + 5*float(self.ids.height.text) - 6.8*float(self.ids.age.text)
            else:
                bmr = 655 + 9.6*float(self.ids.body_mass.text) + 1.8*float(self.ids.height.text) - 4.7*float(self.ids.age.text)
            self.results["Calories"] = int(bmr * self.activity_dict[self.ids.activity.text] * self.goal_dict[self.ids.goal.text])
            self.results["Carbs"] = int(.5*self.results["Calories"]/4)
            self.results["Fats"] = int(.25*self.results["Calories"]/9)
            self.results["Proteins"] = int(.25*self.results["Calories"]/4)
            self.ids.results.text = 'Results: '
            self.print_results()
            self.ids.save_button.disabled = False
        else:
            self.ids.save_button.disabled = True
            self.ids.results.text = 'Results: '
            self.manager.current = 'bad_input'

    def print_results(self):
        for key in self.results:
            if key == "Calories":
                self.ids.results.text += "Calories: " + str(self.results[key]) + "kcal "
            elif key == "Carbs":
                self.ids.results.text += "Carbs: " + str(self.results[key]) + "g "
            elif key == "Fats":
                self.ids.results.text += "Fats: " + str(self.results[key]) + "g "
            else:
                self.ids.results.text += "Proteins: " + str(self.results[key]) + "g"

    def number_input_check(self, my_object):
        text = my_object.text
        try:
            if float(text) <= 0:
                my_object.text = 'Number must be > 0'
            else:
                pass
        except:
            my_object.text = 'Please enter a number!'

    def check_all_inputs(self):
        try:
            float(self.ids.body_mass.text)
            float(self.ids.height.text)
            float(self.ids.age.text)
            if not self.ids.activity.text == 'Level of Activity' and not self.ids.goal == 'Training Goal'\
                    and not self.ids.sex.text == 'Male/Female':
                return True
            else:
                return False
        except:
            return False

    def on_back_without_saving_button_press(self):
        global previous_screen

        self.manager.current = 'menu'
        previous_screen = 'menu'

    def on_back_and_save_button_press(self):
        global user
        global previous_screen

        self.ids.save_button.disabled = True

        user.macros = self.results
        user.body_mass = self.body_mass
        user.height = self.height_attr
        user.age = self.age
        user.sex = self.sex
        user.activity = self.activity
        user.goal = self.goal

        save_user_data(user)

        self.manager.current = 'menu'
        previous_screen = 'menu'


class BadInputScreen(Screen):

    def change_screen_back(self):
        global previous_screen
        self.manager.current = previous_screen


class LinkListScreen(Screen):
    global video_dict
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
                            for video in video_dict.keys():
                                b = Button(text=video, size_hint=(1, None), height=dp(150))
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
        global previous_screen
        previous_screen = 'menu'


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
            global previous_screen
            previous_screen = 'video'
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
        yt = YouTube(video_dict[video_title])
        stream = yt.streams.filter(res='720p').first()
        stream.download(filename='test.mp4')


class NoNetScreen(Screen):

    def change_screen_back(self):
        global previous_screen
        self.manager.current = previous_screen


class VideoScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.removable = ''

    def load_video(self):
        self.ids.video.source = 'test.mp4'
        self.ids.back_button.disabled = False

    def on_back_to_videos_button_press(self):
        global previous_screen
        self.manager.current = 'links'
        previous_screen = 'links'
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
    has_connection = True

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
        self.ids.examples.text = 'Examples'
        self.examples_values = []
        self.examples_dict = {}
        self.added_example_types = set()

    def spinner_clicked(self, value):
        if value not in self.selected_types:
            self.selected_types.append(value)
            self.label_text += value+', '

        self.ids.workout_types_selected.text = self.label_text
        self.check_examples_disability()
        self.examples_values_check_and_fill()

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
        self.examples_values = []
        for value in self.ids.examples.values:
            self.examples_values.append(value)
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
        global previous_screen
        if self.name == 'temp':
            self.name = str(self.workout_id)
            previous_screen = self.name
        else:
            pass

    def on_enter(self, *args):
        for child in self.manager.children:
            if isinstance(child, ExampleVideo):
                self.manager.remove_widget(child)
                del child

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
            self.check_examples_disability()
            self.examples_values_check_and_fill()

    def check_examples_disability(self):
        if len(self.selected_types) > 0:
            self.ids.examples.disabled = False
        else:
            self.ids.examples.disabled = True

    def examples_values_check_and_fill(self):
        if len(self.ids.examples.values) <= 0:
            self.check_internet_connection()
            if self.has_connection:
                self.sql_load()
        else:
            pop_able_keys = []
            for key in self.examples_dict:
                if self.examples_dict[key][1] not in self.selected_types:
                    if self.examples_dict[key][1] in self.added_example_types:
                        self.added_example_types.remove(self.examples_dict[key][1])
                    else:
                        pass
                    pop_able_keys.append(key)
                else:
                    pass
            for key in pop_able_keys:
                self.examples_dict.pop(key)
                self.ids.examples.values.remove(key)
            self.check_internet_connection()
            if self.has_connection and len(self.ids.examples.values) > 0 and len(pop_able_keys) <= 0:
                self.sql_load()
            else:
                pass

    def sql_formatting(self):
        result = ""
        i = 0
        for type in self.selected_types:
            if i == 0:
                if type not in self.added_example_types:
                    result += "styles='"+type+"'"
                    self.added_example_types.add(type)
                    i += 1
                else:
                    pass
            else:
                if type not in self.added_example_types:
                    result += " OR styles='"+type+"'"
                    self.added_example_types.add(type)
                else:
                    pass
        return result

    def sql_load(self):
        mydb = mysql.connector.connect(host='sql11.freemysqlhosting.net', user='sql11434313',
                                       passwd='IPt9fRRDYS')
        mycursor = mydb.cursor()
        mycursor.execute("Select links, titles, styles From sql11434313.Videos Where " + self.sql_formatting())
        myresult = mycursor.fetchall()

        for row in myresult:
            data_list = [row[0], row[2]]
            self.examples_dict[row[1]] = data_list
            self.ids.examples.values.append(row[1])

    def example_selected(self, value):
        self.check_internet_connection()
        if self.has_connection and not value == 'Examples':
            self.download_video(value)
            video_viewer = ExampleVideo(name='example_temp')
            self.manager.add_widget(video_viewer)
            self.manager.current = 'example_temp'

    def download_video(self, video_title):
        yt = YouTube(self.examples_dict[video_title][0])
        stream = yt.streams.filter(res='720p').first()
        stream.download(filename='test.mp4')

    def check_internet_connection(self):
        try:
            mydb = mysql.connector.connect(host='sql11.freemysqlhosting.net', user='sql11434313',
                                           passwd='IPt9fRRDYS', database='sql11434313')
            self.has_connection = True
        except:
            self.has_connection = False
            self.manager.current = 'net'

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


class ExampleVideo(VideoScreen):

    def create_display(self):
        for child in self.children:
            if isinstance(child, BoxLayout):
                box = child
                video = VideoPlayer(id='video', allow_stretch=True)
                button = Button(id='back_button', text='Back to Editor', size_hint=(1, .2), disabled=True)
                button.on_press = self.on_back_to_videos_button_press
                box.add_widget(video)
                box.add_widget(button)

    def on_back_to_videos_button_press(self):
        global previous_screen
        self.manager.current = previous_screen
        self.removable = self.ids.video.source
        self.ids.video.source = ''
        self.ids.video.state = 'stop'
        self.delete_previous_video()
        self.ids.back_button.disabled = True


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
                        "ids.workout_types_selected.text": workout.ids.workout_types_selected.text,
                        "examples_values": workout.examples_values,
                        "examples_dict": workout.examples_dict,
                        "added_example_types": workout.added_example_types}
        save_able_workouts.append(workout_dict)

    with open("save.dat", "wb") as f:
        pickle.dump(save_able_workouts, f)
        pickle.dump(workout_ids, f)


class MenuTestApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (540, 1200)
    # pass


MenuTestApp().run()
