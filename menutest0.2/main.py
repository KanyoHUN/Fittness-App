import os
import certifi
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
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

# All imports above are needed for Application to run!!!

os.environ['SSL_CERT_FILE'] = certifi.where()  # needed to access internet on android


class ScreenManager1(ScreenManager):
    pass


class MenuTestApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (540, 1200)
    # pass


MenuTestApp().run()
