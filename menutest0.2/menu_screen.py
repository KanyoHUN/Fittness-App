from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
import config
import os
import pickle
import mysql.connector
from config import user
from user import save_user_data
from workout_template_screen import WorkoutTemplate


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

    def print_labels(self):  # Can be tinkered with in order to make GUI better!
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
                if float(self.ids.calorie_input.text) > 0:
                    user.macros_used["Calories"] += float(self.ids.calorie_input.text)
                else:
                    i = 100/0
                self.print_labels()
                save_user_data(user)
            except:
                self.manager.current = 'bad_input'
        elif box == self.ids.carb:
            try:
                if float(self.ids.carb_input.text) > 0:
                    user.macros_used["Carbs"] += float(self.ids.carb_input.text)
                else:
                    i = 100/0
                self.print_labels()
                save_user_data(user)
            except:
                self.manager.current = 'bad_input'
        elif box == self.ids.fat:
            try:
                if float(self.ids.fat_input.text) > 0:
                    user.macros_used["Fats"] += float(self.ids.fat_input.text)
                else:
                    i = 100/0
                self.print_labels()
                save_user_data(user)
            except:
                self.manager.current = 'bad_input'
        elif box == self.ids.protein:
            try:
                if float(self.ids.protein_input.text) > 0:
                    user.macros_used["Proteins"] += float(self.ids.protein_input.text)
                else:
                    i = 100/0
                self.print_labels()
                save_user_data(user)
            except:
                self.manager.current = 'bad_input'
        else:
            pass

    def on_minus_button_press(self, box):
        if box == self.ids.calorie:
            try:
                if float(self.ids.calorie_input.text) > 0:
                    if user.macros_used["Calories"] >= float(self.ids.calorie_input.text):
                        user.macros_used["Calories"] -= float(self.ids.calorie_input.text)
                        self.print_labels()
                        save_user_data(user)
                    else:
                        self.ids.calorie_input.text = "Too big number"
                else:
                    i = 100/0
            except:
                self.manager.current = 'bad_input'
        elif box == self.ids.carb:
            try:
                if float(self.ids.carb_input.text) > 0:
                    if user.macros_used["Carbs"] >= float(self.ids.carb_input.text):
                        user.macros_used["Carbs"] -= float(self.ids.carb_input.text)
                        self.print_labels()
                        save_user_data(user)
                    else:
                        self.ids.carb_input.text = "Too big number"
                else:
                    i = 100/0
            except:
                self.manager.current = 'bad_input'
        elif box == self.ids.fat:
            try:
                if float(self.ids.fat_input.text) > 0:
                    if user.macros_used["Fats"] >= float(self.ids.fat_input.text):
                        user.macros_used["Fats"] -= float(self.ids.fat_input.text)
                        self.print_labels()
                        save_user_data(user)
                    else:
                        self.ids.fat_input.text = "Too big number"
                else:
                    i = 100/0
            except:
                self.manager.current = 'bad_input'
        elif box == self.ids.protein:
            try:
                if float(self.ids.protein_input.text) > 0:
                    if user.macros_used["Proteins"] >= float(self.ids.protein_input.text):
                        user.macros_used["Proteins"] -= float(self.ids.protein_input.text)
                        self.print_labels()
                        save_user_data(user)
                    else:
                        self.ids.protein_input.text = "Too big number"
                else:
                    i = 100/0
            except:
                self.manager.current = 'bad_input'
        else:
            pass

    def on_reset_intake_button_press(self):
        user.macros_used = {"Calories": 0, "Carbs": 0, "Fats": 0, "Proteins": 0}
        self.print_labels()
        save_user_data(user)

    def load_workouts(self):
        if not self.workouts_loaded:
            self.workouts_loaded = True
            self.load_able_workouts = []
            if os.path.isfile("save.dat"):
                with open("save.dat", "rb") as file:
                    self.load_able_workouts = pickle.load(file)
                    config.workout_ids = pickle.load(file)

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
                    config.workouts.append(w)

                for worko in config.workouts:
                    b = Button(text=worko.workout_name, font_size=25, size_hint=(1 / 7, (0.8 / 24) * worko.time_difference),
                               pos_hint={"right": 1 / 7 * worko.workout_day, "top": (1 - (.8 / 24) * (worko.start_time-1))})
                    b.on_press = worko.on_workout_button_click
                    config.workout_buttons.append(b)
        else:
            pass

    def on_video_links_button_press(self):
        if not config.video_dict:
            self.check_internet_connection()
            if self.has_connection:
                self.load_video_dict()
                self.manager.current = 'links'
                config.previous_screen = 'links'
            else:
                pass
        else:
            self.manager.current = 'links'
            config.previous_screen = 'links'

    def check_internet_connection(self):
        try:
            mydb = mysql.connector.connect(host='sql11.freemysqlhosting.net', user='sql11434313',
                                           passwd='IPt9fRRDYS', database='sql11434313')
            self.has_connection = True
        except:
            self.has_connection = False
            self.manager.current = 'net'

    def load_video_dict(self):

        mydb = mysql.connector.connect(host='sql11.freemysqlhosting.net', user='sql11434313',
                                       passwd='IPt9fRRDYS', database='sql11434313')
        mycursor = mydb.cursor()
        mycursor.execute("Select links, titles from Videos")
        myresult = mycursor.fetchall()

        for row in myresult:
            config.video_dict[row[1]] = row[0]

    def on_workout_editor_button_press(self):
        self.manager.current = 'editor'
        config.previous_screen = 'editor'

    def on_calorie_calculator_button_press(self):
        self.manager.current = 'input'
        config.previous_screen = 'input'

    def on_nutriments_button_press(self):
        self.manager.current = 'search'
        config.previous_screen = 'search'

    def on_healthy_recipes_button_press(self):
        self.manager.current = 'healthy'
        config.previous_screen = 'healthy'
