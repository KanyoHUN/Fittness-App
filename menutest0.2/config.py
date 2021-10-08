from user import User

previous_screen = 'menu'  # needed for no_net_screen and bad_input_screen change
user = User()  # creating user for storing user data
video_dict = {}  # dictionary of video names(keys) and links(values)
workouts = []  # list of workout_templates
workout_buttons = []  # list of buttons bind to workout_templates
workout_ids = set(())  # set of workout_templates screen names
app_color = ""
