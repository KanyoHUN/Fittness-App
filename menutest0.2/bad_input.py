from kivy.uix.screenmanager import Screen
import config


class BadInputScreen(Screen):

    def change_screen_back(self):
        self.manager.current = config.previous_screen
