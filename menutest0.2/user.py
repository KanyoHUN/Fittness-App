import pickle
import os


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