from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from search import RecipeView, RecipeButtons, SearchScreen
import mysql.connector
import config
from config import user
from user import save_user_data


class HealthyRecipeButtons(RecipeButtons):
    pass


class HealthyRecipeView(RecipeView):
    pass


class RecipeListScreen(Screen):
    recipe_dict = {}
    recipes_loaded = False
    has_connection = True
    screen_added = False
    recipe_name = 'healthy_recipe'
    buttons = []
    result_macros = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recipe = HealthyRecipeView(name=self.recipe_name)

    def on_pre_enter(self, *args):
        if not self.recipes_loaded:
            self.check_internet_connection()
            if self.has_connection:
                self.get_recipes()
                SearchScreen.create_buttons(self)  # Enough to modify it in search.py
                self.add_buttons()
                self.recipes_loaded = True
                self.ids.nonettext.color = (0, 0, 0)
            else:
                self.ids.nonettext.color = (1, 1, 1)

        else:
            pass

    def check_internet_connection(self):
        try:
            mydb = mysql.connector.connect(host=config.host, user=config.database_user,
                                           passwd=config.passwd, database=config.database)
            self.has_connection = True
        except:
            self.has_connection = False

    def get_recipes(self):
        mydb = mysql.connector.connect(host=config.host, user=config.database_user,
                                       passwd=config.passwd, database=config.database)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT name,cal,fat,ch,protein,recipe FROM healthy")
        myresult = mycursor.fetchall()

        for row in myresult:
            self.recipe_dict[row[0]] = [float(row[1]), float(row[2]), float(row[3]), float(row[4]), str(row[5]).replace("/n", "\n")]

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
                                           + str(self.recipe_dict[name][2]) + 'g, Proteins:' + str(
            self.recipe_dict[name][3]) + 'g'
        self.recipe.ids.results.text = 'Results: '
        self.recipe.ids.grams_input.text = ''
        self.display_user_data()
        self.recipe.ids.recipe_text.text = str(self.recipe_dict[name][4])
        self.recipe.ids.Back.text = 'Back To Recipes'
        self.recipe.ids.Back.on_press = self.on_back_to_recipes_button_press

        self.recipe.on_calculate_button_press = self.on_calculate_button_press
        self.recipe.on_add_to_intake_button_press = self.on_add_to_intake_button_press

        self.manager.current = self.recipe_name
        config.previous_screen = self.recipe_name

    def on_back_to_menu_button_press(self):
        SearchScreen.back_to_menu_button_press(self)

    def display_user_data(self):
        SearchScreen.display_user_data(self)  # Enough to modify it in search.py

    def on_add_to_intake_button_press(self):
        SearchScreen.on_add_to_intake_button_press(self)

    def on_calculate_button_press(self):
        SearchScreen.on_calculate_button_press(self)

    def on_back_to_recipes_button_press(self):
        self.manager.current = 'healthy'
        config.previous_screen = 'healthy'

    def add_buttons(self):
        for child_outer in self. children:
            if isinstance(child_outer, ScrollView):
                for child in child_outer.children:
                    if isinstance(child, HealthyRecipeButtons):
                        for button in self.buttons:
                            child.add_widget(button)
