from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
import config
import random
import os
from example_video_screen import ExampleVideo
from save_workouts import save_workouts
import mysql.connector
from pytube import YouTube


class WorkoutTemplate(Screen):
    days_dict = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5,
                 'Saturday': 6, 'Sunday': 7}
    has_connection = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialized = False
        self.selected_types = []
        self.workout_index = len(config.workouts)
        self.workouts_length_on_create = len(config.workouts) + 1
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
        # i have set a hint text for this self.ids.custom_desc.text = 'Customisable workout description.'
        self.workout_id = 0
        self.ids.workout_types_selected.text = 'Selected Workout types: '
        self.ids.examples.text = 'Examples'
        self.examples_values = []
        self.examples_dict = {}
        self.added_example_types = set()

    def spinner_clicked(self, value):
        if value not in self.selected_types:
            self.selected_types.append(value)
            self.label_text += value + ', '

        self.ids.workout_types_selected.text = self.label_text
        self.check_examples_disability()
        self.examples_values_check_and_fill()

    def on_save_workout_button_press(self):
        t_diff = self.end_time - self.start_time
        if self not in config.workouts:
            config.workouts.append(self)
            self.workout_name = self.ids.workout_name_input.text
            while True:
                if self.workout_id == 0:
                    temp = random.randint(1, 200)
                    if temp not in config.workout_ids:
                        config.workout_ids.add(temp)
                        self.workout_id = temp
                        self.name = str(self.workout_id)
                        config.previous_screen = self.name
                        break

        if self.workouts_length_on_create > len(config.workouts):
            diff = self.workouts_length_on_create - len(config.workouts)
            self.workout_index -= diff

        if self.time_difference == 99:
            self.time_difference = t_diff
            button = Button(text=self.workout_name, font_size=1 / 7 * self.width * 0.16,
                            size_hint=(1 / 7, (0.8 / 24) * self.time_difference),
                            pos_hint={"right": 1 / 7 * self.workout_day,
                                      "top": (1 - (.8 / 24) * (self.start_time - 1))},
                            background_color=config.app_color)
            # Here only modify color or texture do not modify size pos etc.
            button.on_press = self.on_workout_button_click
            config.workout_buttons.append(button)
        else:
            self.time_difference = t_diff
            self.workout_name = self.ids.workout_name_input.text
            config.workout_buttons[self.workout_index].text = self.workout_name
            config.workout_buttons[self.workout_index].size_hint = (1 / 7, (0.8 / 24) * self.time_difference)
            config.workout_buttons[self.workout_index].pos_hint = {"right": 1 / 7 * self.workout_day,
                                                                   "top": (1 - (.8 / 24) * (self.start_time - 1))}
        self.examples_values = []
        for value in self.ids.examples.values:
            self.examples_values.append(value)
        self.ids.delete_button.disabled = False
        if os.path.isfile("save.dat"):
            os.remove("save.dat")
        save_workouts()
        self.manager.current = 'editor'
        config.previous_screen = 'editor'

    def on_delete_workout_button_press(self):

        if self.workouts_length_on_create > len(config.workouts):
            diff = self.workouts_length_on_create - len(config.workouts)
            self.workout_index -= diff

        config.workouts.pop(self.workout_index)
        config.workout_buttons.pop(self.workout_index)
        config.workout_ids.remove(self.workout_id)

        if os.path.isfile("save.dat"):
            os.remove("save.dat")
        save_workouts()

        self.manager.current = 'editor'
        config.previous_screen = 'editor'

    def on_back_without_saving_button_press(self):
        self.manager.current = 'editor'
        config.previous_screen = 'editor'

    def on_enter(self, *args):
        for child in self.manager.children:
            if isinstance(child, ExampleVideo):
                self.manager.remove_widget(child)
                del child
        self.check_examples_disability()
        self.examples_values_check_and_fill()
        self.ids.examples.text = 'Examples'

    def on_workout_button_click(self):
        self.manager.current = self.name
        config.previous_screen = self.name

    def on_remove_last_button_press(self):
        if len(self.selected_types) > 0:
            removable = self.selected_types.pop()
            text_len = len(self.label_text)
            for i in range(text_len, text_len - (len(removable) + 2), -1):
                length = len(self.label_text)
                self.label_text = self.label_text[:length - 1]
            self.ids.workout_types_selected.text = self.label_text
            self.check_examples_disability()
            self.examples_values_check_and_fill()

    def check_examples_disability(self):
        self.check_connection_without_change()
        if len(self.selected_types) > 0 and self.has_connection:
            self.ids.examples.disabled = False
        else:
            self.ids.examples.disabled = True

    def examples_values_check_and_fill(self):
        if len(self.ids.examples.values) <= 0 and len(self.selected_types) > 0:
            self.check_connection_without_change()
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
            if len(pop_able_keys) <= 0:
                self.check_connection_without_change()
                if self.has_connection and len(self.ids.examples.values) > 0:
                    self.sql_load()
                else:
                    pass

    def sql_formatting(self):
        result = ""
        i = 0
        for type in self.selected_types:
            if i == 0:
                if type not in self.added_example_types:
                    result += "styles='" + type + "'"
                    self.added_example_types.add(type)
                    i += 1
                else:
                    pass
            else:
                if type not in self.added_example_types:
                    result += " OR styles='" + type + "'"
                    self.added_example_types.add(type)
                else:
                    pass
        return result

    def sql_load(self):
        sql_formated = self.sql_formatting()

        if not sql_formated == "":
            mydb = mysql.connector.connect(host='sql11.freemysqlhosting.net', user='sql11434313',
                                           passwd='IPt9fRRDYS')
            mycursor = mydb.cursor()
            mycursor.execute("Select links, titles, styles From sql11434313.Videos Where " + sql_formated)
            myresult = mycursor.fetchall()

            for row in myresult:
                data_list = [row[0], row[2]]
                self.examples_dict[row[1]] = data_list
                self.ids.examples.values.append(row[1])

    def example_selected(self, value):
        if self.initialized:
            self.check_internet_connection()
            if self.has_connection and not value == 'Examples':
                self.download_video(value)
                video_viewer = ExampleVideo(name='example_temp')
                self.manager.add_widget(video_viewer)
                self.manager.current = 'example_temp'
        else:
            self.initialized = True

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

    def check_connection_without_change(self):
        try:
            mydb = mysql.connector.connect(host='sql11.freemysqlhosting.net', user='sql11434313',
                                           passwd='IPt9fRRDYS', database='sql11434313')
            self.has_connection = True
        except:
            self.has_connection = False

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
            for i in range(self.start_time + 1, 25):
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
