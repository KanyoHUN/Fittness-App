from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

import config


class BadInputScreen(Screen):
    def change_screen_back(self):
        self.manager.current = config.previous_screen
