from functools import partial
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
import mysql.connector
import config
from config import user
from user import save_user_data


class RecipeView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_food_name = ''

    def on_back_to_searching_button_press(self):
        self.manager.current = 'search'
        config.previous_screen = 'search'

    def on_calculate_button_press(self):
        pass

    def on_add_to_intake_button_press(self):
        pass


class SearchScreen(Screen):
    has_connection = True
    buttons = []
    recipe_dict = {}
    screen_added = False
    result_macros = []
    recipe_name = 'recipe'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recipe = RecipeView(name=self.recipe_name)

    def on_search_button_press(self):
        self.check_internet_connection()
        if self.has_connection:
            self.delete_old_search_results()
            if not self.ids.searcher.text == '':
                self.sql_search()
                self.create_buttons()
                self.add_buttons()
            else:
                pass
        else:
            pass

    def sql_formatting(self):
        return "SELECT * FROM food where (name LIKE '%" + self.ids.searcher.text + "%')"

    def sql_search(self):
        mydb = mysql.connector.connect(host='sql11.freemysqlhosting.net', user='sql11434313',
                                       passwd='IPt9fRRDYS', database='sql11434313')
        mycursor = mydb.cursor()
        mycursor.execute(self.sql_formatting())
        myresult = mycursor.fetchall()

        for row in myresult:
            self.recipe_dict[row[1]] = [float(row[2]), float(row[3]), float(row[4]), float(row[5])]

    def check_internet_connection(self):
        try:
            mydb = mysql.connector.connect(host='sql11.freemysqlhosting.net', user='sql11434313',
                                           passwd='IPt9fRRDYS', database='sql11434313')
            self.has_connection = True
        except:
            self.has_connection = False
            self.manager.current = 'net'

    def delete_old_search_results(self):
        deletable_buttons = []
        self.buttons = []
        self.recipe_dict.clear()
        for child_outer1 in self.children:
            if isinstance(child_outer1, BoxLayout):
                for child_outer2 in child_outer1.children:
                    if isinstance(child_outer2, ScrollView):
                        for child_outer3 in child_outer2.children:
                            if isinstance(child_outer3, RecipeButtons):
                                for child in child_outer3.children:
                                    if isinstance(child, Button) and child not in self.buttons and not child.text == 'Back To Menu':
                                        deletable_buttons.append(child)
                                    else:
                                        pass
                                for button in deletable_buttons:
                                    child_outer3.remove_widget(button)
                                    del button

    def create_buttons(self):
        for key in self.recipe_dict:
            b = Button(text=key, size_hint=(1, None), height=dp(150))  # Do not touch text,height or size_hint!
            # But can add more specification for UI customization
            b.on_press = partial(self.food_button_press, key)
            self.buttons.append(b)
        if not self.recipe_dict:
            b = Button(text="No match found!", size_hint=(1, None), height=dp(150))  # Same here.
            self.buttons.append(b)

    def add_buttons(self):
        for child_outer in self.children:
            if isinstance(child_outer, BoxLayout):
                for child in child_outer.children:
                    if isinstance(child, ScrollView):
                        for child_inner in child.children:
                            if isinstance(child_inner, RecipeButtons):
                                for button in self.buttons:
                                    if not button.parent == child_inner:
                                        child_inner.add_widget(button)

    def food_button_press(self, name):
        if not self.screen_added:
            self.manager.add_widget(self.recipe)
            self.screen_added = True
        else:
            pass
        self.recipe.ids.add_button.disabled = True
        self.recipe.current_food_name = name
        self.recipe.ids.food_name.text = 'In 100g ' + name + ':'
        self.recipe.ids.food_macros.text = 'Calories: ' + str(self.recipe_dict[name][0]) + \
            'kcal, Fats: ' + str(self.recipe_dict[name][1]) + 'g, Carbs: ' \
            + str(self.recipe_dict[name][2]) + 'g, Proteins:' + str(self.recipe_dict[name][3]) + 'g'
        self.recipe.ids.results.text = 'Results: '
        self.recipe.ids.grams_input.text = ''
        self.display_user_data()

        self.recipe.on_calculate_button_press = self.on_calculate_button_press
        self.recipe.on_add_to_intake_button_press = self.on_add_to_intake_button_press

        self.manager.current = self.recipe_name
        config.previous_screen = self.recipe_name

    def back_to_menu_button_press(self):
        self.manager.current = 'menu'
        config.previous_screen = 'menu'

    def on_calculate_button_press(self):
        try:
            multiplier = float(self.recipe.ids.grams_input.text)/100
            i = 1
            for item in self.recipe_dict[self.recipe.current_food_name]:
                if i < 5:
                    self.result_macros.append(float('{:.2f}'.format(item*multiplier)))
                i += 1
            self.recipe.ids.results.text = 'Results: Calories: ' + str(self.result_macros[0]) + \
                'kcal, Fats: ' + str(self.result_macros[1]) + 'g, Carbs: ' \
                + str(self.result_macros[2]) + 'g, Proteins:' + \
                str(self.result_macros[3]) + 'g'
            self.recipe.ids.add_button.disabled = False
        except:
            self.manager.current = 'bad_input'

    def on_add_to_intake_button_press(self):
        user.macros_used["Calories"] = float("{:.2f}".format(self.result_macros[0] + user.macros_used["Calories"]))
        user.macros_used["Fats"] = float("{:.2f}".format(self.result_macros[1] + user.macros_used["Fats"]))
        user.macros_used["Carbs"] = float("{:.2f}".format(self.result_macros[2] + user.macros_used["Carbs"]))
        user.macros_used["Proteins"] = float("{:.2f}".format(self.result_macros[3] + user.macros_used["Proteins"]))
        save_user_data(user)
        self.display_user_data()

    def display_user_data(self):  # Here you can modify how you display the user's data but be careful!
        self.recipe.ids.user_data_display.text = 'Calories: ' + str(user.macros_used["Calories"]) + 'kcal/' \
            + str(user.macros["Calories"]) + 'kcal Fats: ' + str(user.macros_used["Fats"]) + 'g/' \
            + str(user.macros["Fats"]) + 'g Carbs: ' + str(user.macros_used["Carbs"]) + 'g/' \
            + str(user.macros["Carbs"]) + 'g Proteins' + str(user.macros_used["Proteins"]) + 'g/' \
            + str(user.macros["Proteins"]) + 'g'


class RecipeButtons(StackLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.bind(minimum_height=self.setter('height'))
