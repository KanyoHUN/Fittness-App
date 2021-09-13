from kivy.graphics import Color, Line
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
import config
import os
from workout_template_screen import WorkoutTemplate


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
            self.parent.manager.current = 'menu'
            config.previous_screen = 'menu'

        def on_add_new_button_press(self):
            new_workout_screen = WorkoutTemplate(name='temp')
            self.parent.manager.add_widget(new_workout_screen)
            self.parent.manager.current = 'temp'
            config.previous_screen = 'temp'

        def on_delete_all_button_press(self):
            len_workouts = len(config.workouts)
            config.workout_buttons = []
            config.workouts = []
            for i in range(0, len_workouts):
                self.parent.add_buttons()

            if os.path.isfile("save.dat"):
                os.remove("save.dat")

    def add_buttons(self):
        for child in self.children:
            if isinstance(child, Button) and child not in config.workout_buttons:
                self.remove_widget(child)
                del child
            else:
                pass

        for child in self.manager.children:
            if isinstance(child, WorkoutTemplate) and child not in config.workouts:
                self.manager.remove_widget(child)
                del child

        for button in config.workout_buttons:
            if not button.parent == self:
                self.add_widget(button)