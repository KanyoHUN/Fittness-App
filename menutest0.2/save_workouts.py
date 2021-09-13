import config
import pickle


def save_workouts():

    save_able_workouts = []

    for workout in config.workouts:
        workout_dict = {"selected_types": workout.selected_types, "workout_index": workout.workout_index,
                        "workouts_length_on_create": workout.workouts_length_on_create,
                        "screen_name": workout.screen_name, "label_text": workout.label_text,
                        "start_time": workout.start_time, "end_time": workout.end_time,
                        "time_difference": workout.time_difference, "workout_day": workout.workout_day,
                        "workout_name": workout.workout_name, "workout_id": workout.workout_id,
                        "ids.start_time_spinner.text": workout.ids.start_time_spinner.text,
                        "ids.end_time_spinner.text": workout.ids.end_time_spinner.text,
                        "ids.workout_day_text.text": workout.ids.workout_day_text.text,
                        "ids.workout_name_input.text": workout.ids.workout_name_input.text,
                        "ids.custom_desc.text": workout.ids.custom_desc.text,
                        "ids.workout_types_selected.text": workout.ids.workout_types_selected.text,
                        "examples_values": workout.examples_values,
                        "examples_dict": workout.examples_dict,
                        "added_example_types": workout.added_example_types}
        save_able_workouts.append(workout_dict)

    with open("save.dat", "wb") as f:
        pickle.dump(save_able_workouts, f)
        pickle.dump(config.workout_ids, f)