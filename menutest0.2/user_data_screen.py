from kivy.uix.screenmanager import Screen
import config
from config import user
from user import save_user_data


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

        self.manager.current = 'menu'
        config.previous_screen = 'menu'

    def on_back_and_save_button_press(self):

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
        config.previous_screen = 'menu'
