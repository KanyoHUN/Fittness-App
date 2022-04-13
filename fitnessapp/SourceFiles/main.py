import os
import certifi
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy import platform
from user import User, save_user_data
from nonet import NoNetScreen
from bad_input import BadInputScreen
import config
from config import user
from save_workouts import save_workouts
from user_data_screen import UserDataScreen
from video_list import LinkListScreen, VideoButtons, VideoScreen
from example_video_screen import ExampleVideo
from workout_template_screen import WorkoutTemplate
from workout_editor_screen import WorkoutEditor
from menu_screen import MenuScreen
from search import SearchScreen, RecipeView, RecipeButtons
from recipes import RecipeListScreen, HealthyRecipeView

# All imports above are needed for Application to run!!!
# IMPORTANT: DO NOT CHANGE ANY ID IN KV FILES!!!!! IT WILL BREAK THE CODE FOR SURE!!!!
os.environ['SSL_CERT_FILE'] = certifi.where()  # needed to access internet on android


def clean_trash():
    file_list = os.listdir()
    for f in file_list:
        if ".mp4" in f:
            os.remove(f)
        else:
            pass


class ScreenManager1(ScreenManager):
    pass


class MenuTestApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config.app_color = self.theme_cls.primary_color
        Window.size = (540, 1200)
        # pass

    def build(self):
        self.theme_cls.theme_style = "Light"


clean_trash()
MenuTestApp().run()
